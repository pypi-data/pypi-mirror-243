from __future__ import annotations

import json
from enum import Enum

from pydantic import BaseModel, ValidationError, Field, validator, root_validator, parse_obj_as, conlist
from pydantic.fields import Validator
import typing as t
from typing_extensions import Annotated


ModelVariable = t.TypeVar("ModelVariable", bound=t.Type[BaseModel])


def optional_discriminators(unions: t.List[str]) -> t.Callable[[ModelVariable], ModelVariable]:
    """:meta private:"""

    def dec(model: ModelVariable) -> ModelVariable:
        for k in unions:
            field = model.__fields__[k]
            discriminator_lookup = {v.type_: k for k, v in field.sub_fields_mapping.items()}

            def handle_missing_discriminator(cls, values):
                if isinstance(values, dict) and field.discriminator_key not in values:
                    parsed = parse_obj_as(t.Union[tuple(f.type_ for f in field.sub_fields)], values)
                    values[field.discriminator_key] = discriminator_lookup[type(parsed)]
                return values

            field.class_validators[f"handle_missing_{field.discriminator_key}"] = Validator(
                handle_missing_discriminator, pre=True
            )
            field.populate_validators()
        return model

    return dec


class Solver(str, Enum):
    """:meta private:"""

    HiGHS = "HiGHS"
    GLPK = "GLPK"
    HiGHS_GLPK = "HiGHS-GLPK"
    GLPK_HiGHS = "GLPK-HiGHS"


class SolverConfig(BaseModel):
    """Parameters that control optimization solver operation

    :meta private:
    """

    solver: Solver = None
    """The solver to use for optimization. Currently supported solvers are: HiGHS, GLPK, HiGHS-GLPK, GLPK-HiGHS
    """
    time_limit: float = 8.0
    """time limit applied to solution of a single optimization window

    - Units: seconds
    - Example: 8 for 8s
    """
    mip_gap_tolerance: float = 0.0
    """relative difference between MIP best integer solution and optimal solution

    For example, to instruct Tyba to stop as soon as it has found a feasible integer solution
    proven to be within five percent of optimal, set the initial_mip_gap_tolerance to 0.05

    - Units: fraction
    - Example: 0.05 for 5% MIP gap tolerance
    """
    verbose: bool = False
    """controls verbosity of solver output"""
    hybrid_infeasible_tol: float = 0
    """TODO"""
    # TODO: document at some point for devs
    solver_specific: t.Dict[str, t.Any] = {}
    """Args to be passed to actual solver. Only allowed when using HiGHS or GLPK solver"""

    initial_time_limit: t.Optional[float] = Field(None, deprecated=True, description="Use time_limit instead")
    initial_mip_gap_tolerance: t.Optional[float] = Field(
        None, deprecated=True, description="Use mip_gap_tolerance instead"
    )
    initial_verbose: t.Optional[bool] = Field(None, deprecated=True, description="Use verbose instead")

    @root_validator(skip_on_failure=True, pre=True)
    def coerce_deprecated_args(cls, values):
        old_to_new = {
            "initial_time_limit": "time_limit",
            "initial_mip_gap_tolerance": "mip_gap_tolerance",
            "initial_verbose": "verbose",
        }
        for k, v in old_to_new.items():
            if values.get(k) is not None:
                if v in values:
                    raise ValueError(f"{k} is deprecated and cannot be provided if {v} is provided")
                else:
                    values[v] = values.pop(k)
        return values

    @validator("time_limit")
    def validate_time_limit(cls, v):
        assert 1e-3 < v < 1e3, f"time_limit must be between 0.001 and 1000 seconds, got {v:.4f} seconds."
        return v

    @validator("mip_gap_tolerance")
    def validate_mip_gap(cls, v):
        assert 0 <= v < 1, f"mip_gap_tolerance must be between 0 and 1, got {v}."
        return v


class StorageCoupling(str, Enum):
    """Enum class for selecting coupling bus for hybrid systems"""

    ac = "ac"
    """indicates the BESS and generator are coupled at the medium voltage AC bus"""
    dc = "dc"
    """indicates the BESS and generator are coupled together at the DC inputs of the generator inverter"""
    hv_ac = "hv_ac"
    """indicates the BESS and generator are coupled at the high voltage AC bus, e.g. the outlet of the GSU/substation"""


class SingleAxisTracking(BaseModel):
    """N-S oriented single axis tracker model"""

    tracking_type: t.Optional[t.Literal["SAT"]] = "SAT"
    """Used by the API for model-type discrimination, can be ignored"""
    rotation_limit: float = 45.0
    """The limit of rotation angle for a single axis tracker. Assumed to be symmetric around 0\ |degrees|
    (tracker horizontal) 

    - Unit: degrees
    - Example: 45 for range of +45\ |degrees| to -45\ |degrees|  
    
    .. |degrees| unicode:: U+00B0
    
    """
    backtrack: bool = True
    """Backtracking eliminates shading between rows of single-axis-tracking arrays (within the :attr:`rotation_limit`)
    by altering the rotation angle of the tracker.

    - Format as a Boolean
    - Example: True to enable backtracking
    """


class FixedTilt(BaseModel):
    """Fixed tilt array model"""

    tracking_type: t.Optional[t.Literal["FT"]] = "FT"
    """Used by the API for model-type discrimination, can be ignored"""
    tilt: float
    """The angle of orientation for a fixed tilt array relative to horizontal, with positive angles tilting the array
    towards the azimuth and negative angles tilting it away.

    - Unit: degrees
    - Example: 30 for 30\ |degrees|
    """


class ScalarUtilization(BaseModel):
    """The quantity of an Ancillary Services capacity award that is dispatched by the grid operator.

    Most operators require sufficient State of Charge to meet AS obligations throughout the day, however the amount
    that a system gets dispatched is unknown in advance. To account for this, we allow you to model a range of
    uncertainty using the following parameters and ensure State of Charge feasibility over an entire horizon.
    Please contact us with further questions on this concept (more detailed explanations coming soon).

    The ScalarUtilization class applies a single uncertainty range for the entire simulation. This is useful for
    scenarios where more detailed utilization information isn't available or accurate. For example, applying historical
    utilization averages to a forecast simulation. To be able to apply utilization ranges as a time series, use
    :class:`TimeSeriesUtilization`
    """

    dimension_type: t.Optional[t.Literal["scalar"]] = "scalar"
    """Used by the API for model-type discrimination, can be ignored"""
    actual: float
    """The modeled dispatched capacity for the base case analysis. 

    - Units: fraction of capacity award for the specific service
    - Example values: 0.20 (20%) for regulation markets, 0.05 (5%) for reserves markets
    """
    lower: float
    """The lower bound dispatched capacity.

    - Units: fraction of capacity award for the specific service
    - Example values: 0.0 indicating no operations 
    """
    upper: float
    """The upper bound dispatched capacity.

    - Units: fraction of capacity award for the specific service
    - Example values: 1.0 (100%) indicating that sufficient state of charge needs to be reserved to meet
      full capacity award.
    """

    @root_validator(skip_on_failure=True)
    def between_0_and_1(cls, values):
        for v in "actual", "lower", "upper":
            assert 0 <= values[v] <= 1, "must be between 0 and 1"
        return values


def _check_lengths(strs_lists: t.Dict[str, list]):
    str1 = next(iter(strs_lists.keys()))
    len1 = len(next(iter(strs_lists.values())))
    for k, v in strs_lists.items():
        assert len(v) == len1, f"{str1} and {k} must be the same length"


class TimeSeriesUtilization(BaseModel):
    """The quantity of an Ancillary Services capacity award that is dispatched by the grid operator.

    The TimeSeriesUtilization class applies a unique utilization scenario to each reserve market time interval.
    This is useful for scenarios with corresponding price and utilization, or when you want to be able to vary the
    utilization over time.

    For more information on utilization generally, see the :class:`ScalarUtilization` docs
    """

    dimension_type: t.Optional[t.Literal["time_series"]] = "time_series"
    """Used by the API for model-type discrimination, can be ignored"""
    actual: t.List[float]
    """The modeled dispatched capacity for the base case analysis. 

    - Units: fraction of capacity award for the specific service
    - Example values: 0.20 (20%) for regulation markets, 0.05 (5%) for reserves markets
    """
    lower: t.List[float]
    """The lower bound dispatched capacity.

    - Units: fraction of capacity award for the specific service
    - Example values: 0.0 indicating no operations
    """
    upper: t.List[float]
    """The upper bound dispatched capacity.

    - Units: fraction of capacity award for the specific service
    - Example values: 1.0 (100%) indicating that sufficient state of charge needs to be reserved to meet
      full capacity award.
    """

    @root_validator(skip_on_failure=True)
    def between_0_and_1(cls, values):
        for v in "actual", "lower", "upper":
            assert all(0 <= vi <= 1 for vi in values[v]), "must be between 0 and 1"
        return values

    @root_validator(skip_on_failure=True)
    def check_length(cls, values):
        _check_lengths({"actual": values["actual"], "lower": values["lower"], "upper": values["upper"]})
        return values

    def __len__(self) -> int:
        return len(self.actual)


@optional_discriminators(["utilization"])
class ReserveMarket(BaseModel):
    """General class for different types of Ancillary Services.

    This will be a dictionary item in either the ``up`` or ``down`` field of :class:`ReserveMarkets` depending on the
    service.
    """

    price: t.List[float]
    """The capacity prices for this specific service. Used in dispatch co-optimization. Assumed to be hourly. The
    list length must be equivalent to the hourly sum of all battery terms.

    - Units: $/MW
    - Values length: if the project is a 1-year project, the list must be 8760-values long
    """
    offer_cap: float
    """The maximum storage capacity that can be bid for this specific service in each interval. Specific offer values
    will be allocated by the dispatch optimization algorithm. Assumed to be hourly. The
    list length must be equivalent to the hourly sum of all battery terms.

    - Units: MW
    - Maximum value: 200% of nameplate power
    """
    utilization: t.Union[ScalarUtilization, TimeSeriesUtilization] = Field(..., discriminator="dimension_type")
    """Sub-model to account for utilization uncertainty. See :class:`ScalarUtilization`. If using
    :class:`TimeSeriesUtilization`, must be same length as :attr:`price`.
    """
    duration_requirement: float = Field(0.0, description="market requirement for offer duration (hours)")
    """The duration for which a reserve offer must be sustainable, given a BESS’s SOE. For example, for a
    duration_requirement of 1 hour, a 10MW / 2hr battery with a current SOE of 5MWh would only be allowed to offer
    5MW to the reg-up market, as this is the output it could sustain for 1 hour. This only applies to “up” markets.

    - Units: hours
    - Default: 0 hours
    - Recommended values:
      - ERCOT reg-up: 1 hour
      - ERCOT reserves (RRS): 1 hour
    """
    obligation: t.Optional[t.List[float]]
    """Time series of already-cleared reserve market obligations. If provided, reserve markets participation is treated
    as a constraint on real-time market participation, instead of reserve market participation being co-optimized. 
    
    - Assumed to be hourly
    - Must have same length as :attr:`price`
    - Positive-only values
    - Units: kW
    """

    @root_validator(skip_on_failure=True)
    def check_length(cls, values):
        if isinstance(values["utilization"], TimeSeriesUtilization):
            _check_lengths({"price": values["price"], "utilization": values["utilization"]})
        if values["obligation"]:
            _check_lengths({"price": values["price"], "obligation": values["obligation"]})
        return values

    def __len__(self) -> int:
        return len(self.price)


class ReserveMarkets(BaseModel):
    """Container for holding ancillary/reserve market inputs"""

    up: t.Optional[t.Dict[str, ReserveMarket]]
    """dictionary of reserve markets, where each key is the market name and the corresponding value is the
    :class:`ReserveMarket` object.
    
    For example:
    
    .. code-block:: python

        {
            'reg_up': ReserveMarket(...),
            'rrs': ReserveMarket(...)
        }
    """
    down: t.Optional[t.Dict[str, ReserveMarket]]
    """dictionary of reserve markets, where each key is the market name and the corresponding value is the
        :class:`ReserveMarket` object. See :attr:`up` for example
    """

    @root_validator(skip_on_failure=True)
    def check_length(cls, values):
        length = None
        for attrib in "up", "down":
            for v in (values[attrib] or dict()).values():
                if length is None:
                    length = len(v)
                else:
                    assert len(v) == length, "all reserve markets must contain data of the same length"
        return values

    def __len__(self) -> int:
        for v in (self.up or dict()).values():
            return len(v)


class DARTPrices(BaseModel):
    """Energy prices used for the energy arbitrage application."""

    rtm: conlist(float, min_items=1)
    """Real-time market prices. Prices correspond to the time interval given by :attr:`MarketBase.time_interval_mins`.
    The list length must match the sum of all battery terms when given in the chosen time interval.
        
    - For example: if the project has 2 batteries, each with a 1-year term, and the chosen interval is 15min,
      the list must be (2 battery years) * (8760*4 intervals per year) = 70080 values long
    """
    dam: conlist(float, min_items=1)
    """Hourly Day-Ahead prices. The list length must match the hourly sum of all battery terms.
        
    - For example: if the project is a 1-year, hourly project, the list must be 8760-values long
    """
    imbalance: t.Optional[conlist(float, min_items=1)]
    """Imbalance market or payment prices. Intended for modeling e.g. ERCOT's Real Time On-line Reserve Price Adder
    (RTORPA). Prices correspond to the time interval given by :attr:`MarketBase.time_interval_mins` and list length
    must match :attr:`rtm`
    """
    rtorpa: t.Optional[conlist(float, min_items=1)]  # this attribute gets dropped on instantiation
    """Deprecated, replaced with :attr:`imbalance`"""

    @root_validator(skip_on_failure=True)
    def check_imbalance(cls, values):
        if values["rtorpa"]:
            if values["imbalance"]:
                raise ValueError("Only one of 'rtorpa' and 'imbalance' may be provided")
            values["imbalance"] = values["rtorpa"]
        if values["imbalance"]:
            assert len(values["imbalance"]) == len(values["rtm"]), "Imbalance must have same length as RTM"
        del values["rtorpa"]
        return values


def _check_time_interval(sub_hourly, hourly, time_interval_mins, subhourly_str, hourly_str):
    rt_intervals_per_hour, err = divmod(len(sub_hourly), len(hourly))
    assert err == 0, f"length of {hourly_str} must divide length of {subhourly_str}"
    assert (
        60 / rt_intervals_per_hour == time_interval_mins
    ), f"lengths of {subhourly_str} and {hourly_str} must reflect time_interval_mins"


class DARTPriceScenarios(BaseModel):
    """:meta private:"""

    # TODO: Still want docstrings for devs at some point
    rtm: conlist(conlist(float, min_items=1), min_items=1)
    dam: conlist(conlist(float, min_items=1), min_items=1)
    weights: t.List[float]

    @root_validator(skip_on_failure=True)
    def check_lengths(cls, values):
        assert len(values["dam"]) == len(values["rtm"]) == len(values["weights"])
        return values

    def __len__(self):
        return len(self.rtm[0])


class MarketBase(BaseModel):
    """Base class for Model classes with market-based optimization"""

    energy_prices: t.Union[DARTPrices, t.List[float], DARTPriceScenarios]
    """The energy prices used for storage dispatch optimization. This can either be a single energy price timeseries or
    two energy price timeseries (i.e corresponding to DA & RT markets):

    - Single energy market timeseries: Provide a list of prices. Prices correspond to the time interval given by
      :attr:`time_interval_mins`. The list length must match the sum of all battery terms when given in the chosen
      time interval. For example: if the project is a 1-year, hourly project, the list should be 8760 values long.
      A half-year term modeled with a time interval of 15 minutes, requires a list of 17520 energy prices.
    - Two energy market timeseries: Provide a :class:`DARTPrices` object
    """
    reserve_markets: t.Optional[ReserveMarkets] = None
    """A sub-model to handle the specification of reserve market/ancillary market inputs.
    """
    time_interval_mins: t.Optional[int] = 60
    """The number of minutes per real-time market interval.

    - Use 60 for an hourly run
    - Use 5 for a five-minute run

    Note: :attr:`StorageSolverOptions.window` and :attr:`StorageSolverOptions.step` values will adjust accordingly
    """
    load_peak_reduction: t.Optional[LoadPeakReduction] = None
    """A sub-model to handle the specification of load reduction inputs
    """
    dam_award: t.Optional[t.List[float]] = None
    """List of system dispatch values awarded in the day ahead market. These values are used when re-optimizing
    real-time market operations.
    
    - Units are kW
    - Positive values represent system export
    - Time interval is assumed to be hourly corresponding with Day Ahead market 
    
    :meta private:
    """

    @root_validator(skip_on_failure=True)
    def validate_dam_award(cls, values):
        if values["dam_award"] is not None:
            assert isinstance(
                values["energy_prices"], (DARTPrices, DARTPriceScenarios)
            ), "When providing a dam_award, separate DAM and RTM prices are required."
            if isinstance(values["energy_prices"], DARTPriceScenarios):
                rtm_prices = values["energy_prices"].rtm[0]
            else:
                rtm_prices = values["energy_prices"].rtm
            _check_time_interval(
                sub_hourly=rtm_prices,
                hourly=values["dam_award"],
                time_interval_mins=values["time_interval_mins"],
                subhourly_str="rtm prices",
                hourly_str="dam awards",
            )
        return values

    @root_validator(skip_on_failure=True)
    def check_time_interval(cls, values):
        if isinstance(values["energy_prices"], DARTPrices):
            _check_time_interval(
                values["energy_prices"].rtm,
                values["energy_prices"].dam,
                values["time_interval_mins"],
                "rtm prices",
                "dam prices",
            )
        return values

    @root_validator(skip_on_failure=True)
    def check_length(cls, values):
        if values["reserve_markets"]:
            if isinstance(values["energy_prices"], DARTPriceScenarios):
                dam_prices = values["energy_prices"].dam[0]
            else:
                dam_prices = values["energy_prices"].dam
            _check_lengths(
                {
                    "dam prices": dam_prices,
                    "reserve market data": values["reserve_markets"],
                }
            )

        if values["load_peak_reduction"]:
            _check_lengths(
                {"rtm prices": values["energy_prices"].rtm, "peak reduction data": values["load_peak_reduction"]}
            )
        return values


class SolarResourceTimeSeries(BaseModel):
    """Irradiance and environmental time series data

    - The interval for all time series is assumed to match :attr:`PVGenerationModel.time_interval_mins`.
    - All time-series must be the same length.
    - For sub-hourly data, the timestamp represented by the ``year``, ``month``, ``day``, ``hour`` and ``minute``
      attributes represents the beginning of the time interval, as well as the time to be used for sun position
      calculations. For hourly data, the beginning of the time interval is given by :attr:`hour`. :attr:`minute`
      indicates the point within the interval to be used for determining sun position.
    - The irradiance and weather values represent average values across the interval. Timestamps are assumed to be in
      local *standard* time and should not consider Daylight Savings Time or include leap days. To model a leap day
      (e.g. for a back-cast with aligned price and irradiance data), repeat timestamps for 2/28.
    - Typical Year (TY) solar resource data is assumed to represent the "typical" resource in a location such that the
      data can be tiled across all the years of a project's lifetime. If data is for a Typical Year (TY) and is
      intended to be tiled, it must:
       - represent one full year of data (8760 hours)
       - not contain any leap days
       - start with the 0th hour of January 1st.
    """

    year: t.List[int]
    """Year value of the interval-beginning timestamp
    
    - 4 digit integer.
    """
    month: t.List[int]
    """Month value of interval-beginning timestamp
        
    - Possible values: 1-12.
    """
    day: t.List[int]
    """Day value of interval-beginning timestamp
        
    - Possible values: 1-31
    """
    hour: t.List[int]
    """Hour value of interval-beginning timestamp
        
    - Possible values: 0-23
    """
    minute: t.List[int]
    """Minute values of interval-beginning timestamp, or for hourly simulations, the minute associated with desired sun
    position
    
    - Possible values: 0-59
    - For hourly simulations, in almost all cases, this should be 30 for all intervals (the midpoint of the hour) 
    """
    tdew: t.List[float]
    """Dew point temperature

    - Units: |degrees|\ C
    """
    df: t.List[float]
    """`Diffuse Horizontal Irradiance <df_>`_
    
    .. _df: https://pvpmc.sandia.gov/modeling-steps/1-weather-design-inputs/irradiance-and-insolation-2/diffuse-
        horizontal-irradiance/

    - Units: W/m\ :sup:`2`
    """
    dn: t.List[float]
    """`Direct Normal Irradiance <dn_>`_
    
    .. _dn: https://pvpmc.sandia.gov/modeling-steps/1-weather-design-inputs/irradiance-and-insolation-2/direct-
        normal-irradiance/

    - Units: W/m\ :sup:`2`
    """
    gh: t.List[float]
    """`Global Horizontal Irradiance <gh_>`_
    
    .. _gh: https://pvpmc.sandia.gov/modeling-steps/1-weather-design-inputs/irradiance-and-insolation-2/global-
        horizontal-irradiance/

    - Units: W/m\ :sup:`2`
    """
    pres: t.List[float]
    """Ambient pressure

    - Units: milibar
    """
    tdry: t.List[float]
    """Ambient Temperature (dry bulb)

    - Units: |degrees|\ C
    """
    wdir: t.List[float]
    """Wind direction

    - Units: degrees east of north, with a wind from the north having a value of 0.0
    """
    wspd: t.List[float]
    """Wind speed

    - Units: meter per second
    """
    alb: t.Optional[t.List[float]]
    """`Surface albedo <alb_>`_
    
    .. _alb: https://pvpmc.sandia.gov/modeling-steps/1-weather-design-inputs/plane-of-array-poa-irradiance/
        calculating-poa-irradiance/poa-ground-reflected/albedo/

    - Units: ratio of reflected GHI
    - Default value is 0.2
    """
    snow: t.Optional[t.List[float]]
    """Snow depth

    - Units: centimeters
    """

    @root_validator(skip_on_failure=True)
    def check_lengths(cls, values):
        try:
            _check_lengths({k: v for k, v in values.items() if v is not None})
        except AssertionError:
            raise AssertionError("solar resource time series data must have consistent lengths")
        return values

    def __len__(self) -> int:
        return len(self.year)


class SolarResource(BaseModel):
    """Sub-model for full specification of solar resource inputs"""

    latitude: float
    """Geographic coordinate for the North-South position of the resource in decimal degrees 

    - Example: 38.0 for 38.0\ |degrees|\ N
    """
    longitude: float
    """Geographic coordinate for the East-West position of the resource in decimal degrees

    - Example: -80.0 for 80.0\ |degrees|\ W
    """
    time_zone_offset: float
    """The UTC offset for the amount of time subtracted from or added to the UTC timezone. This is used in conjuction
    with the local-standard timestamps contained in :attr:`data`

    - Example: -8.0 for UTC-8:00 (Pacific Standard Time)
    """
    elevation: float
    """Height above (or below) sea level.

    - Units: meters
    - Example: 358.0 for 358 meters above sea level
    """
    data: SolarResourceTimeSeries
    """Solar resource time series data, see :class:`SolarResourceTimeSeries` for gotchas (e.g. Typical Year constraints)
    """
    monthly_albedo: t.Optional[t.List[float]]
    """Surface albedo is the fraction of the Global Horizontal Irradiance that reflects, `more detail here <alb_>`_.
    If provided, this value overrides the hourly albedo value in SolarResourceTimeSeries.

    - Units: ratio
    - Format as a 12 element list of floats
    - Example: [0.2] * 12 for 12 months of 0.2 albedo
    - Default value is 0.2
    """

    def __len__(self) -> int:
        return len(self.data)


class PSMRegion(str, Enum):
    """Enum class for selecting world region when pulling PSM solar resource data"""

    NorthAmerica = "North America"
    """Selects the North American dataset"""
    AsiaPacific = "Asia/Pacific"
    """Selects the North American dataset"""


class SolarResourceLocation(BaseModel):
    """Location inputs class for pulling PSM solar resource data from the `NSRDB <https://nsrdb.nrel.gov/>`__"""

    latitude: float
    """Geographic coordinate for the North-South position of the resource in decimal degrees 

    - Example: 38.0 for 38.0\ |degrees|\ N
    """
    longitude: float
    """Geographic coordinate for the East-West position of the resource in decimal degrees

    - Example: -80.0 for 80.0\ |degrees|\ W
    """
    region: PSMRegion = PSMRegion.NorthAmerica
    """regional data set to be queried"""

    class Config:
        extra = "forbid"


class FileComponent(BaseModel):
    """Equipment inputs class for using inverter/pv module files that have already been uploaded to Tyba, e.g. via
    the Webapp
    """

    path: str
    """Path in Tyba database to uploaded file. Please contact Tyba for assistance in determining the correct file path
    """


class PVModuleCEC(BaseModel):
    """Inputs for modeling PV module/array performance using the CEC module model, which is an extension of the
    `Desoto 5-parameter model <desoto_>`_. More information on how the model is implemented in NREL SAM (and by
    extension Tyba) can be found in Section 10.4 of the
    `SAM Photovoltaic Model Technical Reference Update <sam_tech_ref_>`_.

    .. _desoto: https://pvpmc.sandia.gov/modeling-steps/2-dc-module-iv/single-diode-equivalent-circuit-models/de-soto-
        five-parameter-module-model/
    .. _sam_tech_ref: https://www.nrel.gov/docs/fy18osti/67399.pdf
    """

    bifacial: bool
    """Whether or not the module is bifacial"""
    a_c: float
    """Module area

    - Units: m\ :sup:`2`
    - Example value: 2.17 m\ :sup:`2`
    """
    n_s: float
    """Number of cells

    - Example value: 72
    """
    i_sc_ref: float
    """Short circuit current at STC

    - Units: Adc
    - Example value: 11.3 Adc
    """
    v_oc_ref: float
    """Open circuit voltage at STC

    - Units: Vdc
    - Example value: 48.6 Vdc
    """
    i_mp_ref: float
    """Max power current at STC

    - Units: Adc
    - Example value: 10.8 Adc
    """
    v_mp_ref: float
    """Max power voltage at STC

    - Units: Vdc
    - Example value: 40.1Vdc
    """
    alpha_sc: float
    """Temperature coefficient of short circuit current

    - Denormalize the CEC Data-sheet :math:`\\alpha` value as follows:
        - :math:`\\alpha = {\\alpha_{CEC}}*{I_{sc}/100}`
    - Units: A/K
    - Example value: 0.00461 A/K
    """
    beta_oc: float
    """Temperature coefficient of open circuit voltage

    - Denormalize the CEC Data-sheet :math:`\\beta` value as follows:
        - :math:`\\beta = {\\beta_{CEC}}*{V_{oc}/100}`
    - Units: V/K
    - Example value: -0.1406 V/K
    """
    t_noct: float
    """Nominal operating cell temperature

    - Units: |degrees|\ C
    - Example value: 44.0\ |degrees|\ C
    """
    a_ref: float
    """Ideality factor at STC

    - Units: V
    - Example value: 1.81 V
    """
    i_l_ref: float
    """Light current at STC

    - Units: A
    - Example value: 11.47 A
    """
    i_o_ref: float
    """Diode saturation current at STC

    - Units: A
    - Example value: 2.63e-11 A
    """
    r_s: float
    """Reference series resistance
    
    - Units: :math:`\\Omega`
    - Example value: 0.27\ :math:`\\Omega`
    """
    r_sh_ref: float
    """Reference shunt resistance

    - Units: :math:`\\Omega`
    - Example value: 453.56\ :math:`\\Omega`
    """
    adjust: float
    """Temperature coefficient adjustment factor

    - Format as a float that represents the percentage
    - Example value: 7.64 for 7.64%
    """
    gamma_r: float
    """Temperature coefficient of maximum power

    - Units:  %/\ |degrees|\ C
    - Example value: -0.36%/\ |degrees|\ CC
    """
    bifacial_transmission_factor: float
    """Fraction of irradiance incident on the front surface of the array that passes through and strikes the ground
    (and thus contributes to backside irradiance). Such transmission can be due to e.g. gaps between modules,
    module/cell borders for glass-glass modules etc. Sometimes estimated as the ratio of the area light can pass
    through to the total bounding area of the array frontside collector surface

    - Ignored if :attr:`bifacial` is ``False``
    - Format as a float that represents the decimal value
    - Example value: 0.2 for 20%
    """
    bifaciality: float
    """Rear-side to front-side efficiency ratio. 

    - Ignored if :attr:`bifacial` is ``False``
    - Format as a float that represents the decimal value
    - Example value: 0.68 for 68%
    """
    bifacial_ground_clearance_height: float
    """Height from the ground to the bottom of the PV array. For tracking systems, this is the height at a zero-degree
    tilt

    - Ignored if :attr:`bifacial` is ``False``
    - Units: m
    - Example value: 0 m
    """


class MermoudModuleTech(str, Enum):
    """Enum class for selecting module technology input to :attr:`PVModuleMermoudLejeune.tech`"""

    SiMono = "mtSiMono"
    """Monocrystalline Silicon"""
    SiPoly = "mtSiPoly"
    """Polycrystalline Silicon"""
    CdTe = "mtCdTe"
    """Thin-film Cadmium-Telluride"""
    CIS = "mtCIS"
    """Copper Indium Gallium Selenide"""
    uCSi_aSiH = "mtuCSi_aSiH"
    """Amorphous Silicon"""


class PVModuleMermoudLejeune(BaseModel):
    """Inputs for modeling PV module/array performance using the `Mermoud-Legeune (aka PVsyst) model <mermoud_>`_.
    Instances can be generated from PAN files using :func:`tyba_client.io.pv_module_from_pan`

    .. _mermoud: https://pvpmc.sandia.gov/modeling-steps/2-dc-module-iv/single-diode-equivalent-circuit-models/
        pvsyst-module-model/
    """

    bifacial: bool
    """Whether or not the module is bifacial"""
    bifacial_transmission_factor: float
    """Fraction of irradiance incident on the front surface of the array that passes through and strikes the ground
        (and thus contributes to backside irradiance). Such transmission can be due to e.g. gaps between modules,
        module/cell borders for glass-glass modules etc. Sometimes estimated as the ratio of the area light can pass
        through to the total bounding area of the array frontside collector surface

    - Ignored if :attr:`bifacial` is ``False``
    - Format as a float that represents the decimal value
    - Example value: 0.2 for 20%
    """
    bifaciality: float
    """Rear-side to front-side efficiency ratio. 

    - Ignored if :attr:`bifacial` is ``False``
    - Format as a float that represents the decimal value
    - Example value: 0.68 for 68%
    """
    bifacial_ground_clearance_height: float
    """Height from the ground to the bottom of the PV array. For tracking systems, this is the height at a zero-degree
        tilt

    - Ignored if :attr:`bifacial` is ``False``
    - Units: m
    - Example value: 0 m
    """
    tech: MermoudModuleTech
    """Input for selecting module technology, which determines :math:`E_g` and :math:`\\frac{d^2}{\\mu_{\\tau, eff}}`
    used in the single diode equation. Values are chosen based on recommendations in the
    `PVSyst User Guide <pvsyst_guide_module_model_>`_. Note that a custom value for
    :math:`\\frac{d^2}{\\mu_{\\tau, eff}}` can also be provided with the :attr:`custom_d2_mu_tau` input.
    
    .. _pvsyst_guide_module_model: https://www.pvsyst.com/help/index.html?pvmodule_model.htm
    """
    iam_c_cs_iam_value: t.Optional[t.List[float]]
    """Incident angle modifier factors

    - Corresponds to :attr:`iam_c_cs_inc_angle`
    - Units: unitless
    - Example values: [1.0, 1.0, 0.95, 0.85, 0.6, 0.2, 0.]
    """
    iam_c_cs_inc_angle: t.Optional[t.List[float]]
    """Incident angle modifier angles

    - Corresponds to :attr:`iam_c_cs_iam_value`
    - Units: degrees
    - Example values: [0, 15, 30, 45, 60, 75, 90]
    """
    i_mp_ref: float
    """Max power current at reference conditions (set by :attr:`s_ref` and :attr:`t_ref`)

    - Units: Adc
    - Example value: 10.8 Adc
    """
    i_sc_ref: float
    """Short circuit current at reference conditions (set by :attr:`s_ref` and :attr:`t_ref`)

    - Units: Adc
    - Example value: 11.3 Adc
    """
    length: float
    """Long dimension of solar module

    - Units: m
    - Example value: 1.956m
    """
    n_diodes: int
    """Number of diodes in solar cell

    - Units: quantity
    - Example value: 3
    """
    n_parallel: int
    """Number of cells in parallel

    - Units: quantity
    - Example value: 1
    """
    n_series: int
    """Number of cells in series

    - Units: quantity
    - Example value: 72
    """
    r_s: float
    """Reference series resistance
    
    - Units: :math:`\\Omega`
    - Example value: 0.27
    """
    r_sh_0: float
    """Shunt resistance in 0 irradiance

    - Units: :math:`\\Omega`
    - Example value: 2500
    """
    r_sh_exp: float
    """Shunt resistance exponential factor

    - Units: :math:`\\Omega`
    - Example value: 5.5
    """
    r_sh_ref: float
    """Shunt resistance at reference conditions (set by :attr:`s_ref` and :attr:`t_ref`)

    - Units: :math:`\\Omega`
    - Example value: 600
    """
    s_ref: float
    """Reference irradiance. In almost all cases this should be 1000 W/m\ :sup:`2` corresponding to STC 

    - Units: W/m\ :sup:`2`
    - Example value: 1000
    """
    t_c_fa_alpha: float
    """Faiman thermal model absorptivity. Referred to as "Alpha" in the `PVsyst User Guide <pvsyst_guide_thermal_>`_.
    
    .. _pvsyst_guide_thermal: https://www.pvsyst.com/help/thermal_loss.htm

    - Units: unitless
    - Example value: 0.90
    """
    t_ref: float
    """Reference temperature. In almost all cases this should be 25\ |degrees|\ C corresponding to STC

    - Units: |degrees|\ C
    - Example value: 25.0
    """
    v_mp_ref: float
    """Max power voltage at reference conditions (set by :attr:`s_ref` and :attr:`t_ref`)

    - Units: Vdc
    - Example value: 40.1Vdc
    """
    v_oc_ref: float
    """Open circuit voltage at reference conditions (set by :attr:`s_ref` and :attr:`t_ref`)

    - Units: Vdc
    - Example value: 48.6Vdc
    """
    width: float
    """Short dimension of solar module

    - Units: m
    - Example value: 0.992 m
    """
    alpha_sc: float
    """Temperature coefficient of short circuit current

    - Units: A/K
    - Example value: 0.00461 A/K
    """
    beta_oc: float
    """Temperature coefficient of open circuit voltage

    - Units: V/K
    - Example value: -0.1406 V/K
    """
    mu_n: float
    """Temperature coefficient of diode non-ideality factor

    - Units: 1/K
    - Example value: -0.0007 1/K
    """
    n_0: float
    """Diode non-ideality factor

    - Units: 1/K
    - Example value: 0.967
    """
    custom_d2_mu_tau: t.Optional[float]
    """Custom recombination loss coefficient. If not set, the value of :math:`\\frac{d^2}{\\mu_{\\tau, eff}}` is chosen
    based on :attr:`tech`

    - Units: V
    - Example value: 1.4 V
    """


class BaseInverter(BaseModel):
    """Base class for inverter model input classes"""

    mppt_low: float
    """Minimum MPPT DC Voltage

    - Units: Vdc
    - Example value: 1003 Vdc
    """
    mppt_high: float
    """Maximum MPPT DC Voltage

    - Units: Vdc
    - Example value: 1200 Vdc
    """
    paco: float
    """Maximum AC power

    - Units: Wac
    - Example value: 4198240 Wac
    """
    vdco: float
    """Nominal DC Voltage

    - Units: Vdc
    - Example value: 1062 Vdc
    """
    pnt: float
    """Standby/Nighttime power use

    - Units: Wac
    - Example value: 1259.47 Wac
    """
    includes_xfmr: bool = False
    """Indicate whether inverter model includes a medium voltage transformer. If set to ``True``, then
    :attr:`ACLosses.mv_transformer` should be ``None`` or MV transformer losses will be double counted.
    """


class Inverter(BaseInverter):
    """Inputs for modeling inverter performance using the `Sandia Inverter Model <sandia_inverter_>`_.

    .. _sandia_inverter: https://pvpmc.sandia.gov/modeling-steps/dc-to-ac-conversion/sandia-inverter-model/
    """

    pso: float
    """Power use during operation

    - Units: Wdc
    - Example value: 6429 Wdc
    """
    pdco: float
    """Maximum DC power

    - Units: Wdc
    - Example value: 4272031 Wdc
    """
    c0: float
    """First Sandia Coefficients

    - Units: 1/Wac
    - Example value: 2.84059e-9  1/Wac
    """
    c1: float
    """Second Sandia Coefficient

    - Units: 1/Vdc
    - Example values: 1.1e-5
    """
    c2: float
    """Third Sandia Coefficient

    - Units: 1/Vdc
    - Example values: 0.001713
    """
    c3: float
    """Fourth Sandia Coefficient

    - Units: 1/Vdc
    - Example values: 0.001056
    """
    vdcmax: float
    """Maximum DC Voltage

    - Units: Vdc
    - Example value: 1200 Vdc
    """


class ONDTemperatureDerateCurve(BaseModel):
    """Temperature derate inputs for use with :class:`ONDInverter`. Maximum AC power is assumed to vary linearly
    between the points, as explained in the `PVSyst User Guide <pvsyst_inv_temp_derate_>`_.

    .. _pvsyst_inv_temp_derate: https://www.pvsyst.com/help/index.html?inverter_outputparameter.htm
    """

    ambient_temp: t.List[float]
    """Temperatures in the derate curve, corresponding to :attr:`max_ac_power`
    
    - Units: |degrees|\ C
    - Example values: [25.0, 50.0, 60.0]
    """
    max_ac_power: t.List[float]
    """Maximum AC output values in the derate  curve, corresponding to :attr:`ambient_temp`
    
    - Units: W
    - Example values: [14000, 12000, 10000]
    """


class ONDEfficiencyCurve(BaseModel):
    """Efficiency curve inputs for use with :class:`ONDInverter`"""

    dc_power: t.List[float]
    """List of input DC power values. First value must equal to :attr:`ONDInverter.dc_turn_on`
    
    - Units: W
    - Examples values: [0.0, 200.0, 300.0, 600.0, 1000.0]
    """
    ac_power: t.List[float]
    """List of output AC power values corresponding to the values in :attr:`dc_power`
    
    - Units: W
    - Example values: [0.0, 199.0, 298.0, 596.0, 1090.0]
    """


class ONDInverter(BaseInverter):
    """Inputs for modeling inverter performance using the `PVSyst/OND model <pvsyst_inv_>`_. Instances can be
    generated from OND files using :func:`tyba_client.io.inverter_from_ond`.

    .. _pvsyst_inv: https://www.pvsyst.com/help/index.html?inverter_inputmodel.htm
    """

    temp_derate_curve: ONDTemperatureDerateCurve
    """Curve of maximum AC power vs ambient temperature"""
    nominal_voltages: t.List[float]
    """DC voltage values that correspond to the curves provided in :attr:`power_curves`. Must have 3 voltages.
    
    - Units: Vdc
    - Example values: [900.0, 1200.0, 1500.0]
    """
    power_curves: t.List[ONDEfficiencyCurve]
    """DC vs AC power curves that correspond to the dc voltages in :attr:`nominal_voltages`. Must have 3 curves. First
    DC power value in each curve must equal to :attr:`dc_turn_on`
    """
    dc_turn_on: float
    """Minimum DC power value that must be provided for AC power to be produced by inverter.
    
    - Units: W
    - Example value: 100.0
    """
    aux_loss: t.Optional[float]
    """Additional losses applied after efficiency and temperature derate when DC power is above
    :attr:`aux_loss_threshold`. This can be used to represent e.g. fan losses and should be based on manufacturer
    recommendations.
    
    - Units: W
    - Example value: 100.0
    """
    aux_loss_threshold: t.Optional[float]
    """DC power threshold above which the loss in :attr:`aux_loss` gets applied.
    
    - Units: W
    - Example value: 200.0
    """

    @root_validator(skip_on_failure=True)
    def check_sufficient_power_curves_voltages(cls, values):
        assert (
            len(values["power_curves"]) == len(values["nominal_voltages"]) == 3
        ), "3 power curves and corresponding voltages required for OND model"
        return values

    @root_validator(skip_on_failure=True)
    def check_aux_loss_etc(cls, values):
        if (values.get("aux_loss") is None) != (values.get("aux_loss_threshold") is None):
            raise AssertionError("either both or neither of aux_loss and aux_loss_threshold must be provided")
        return values


InverterTypes = t.Union[Inverter, ONDInverter, str, FileComponent]
PVModuleTypes = t.Union[PVModuleCEC, PVModuleMermoudLejeune, str, FileComponent]


class Layout(BaseModel):
    """Inputs related to the configuration of PV modules within their racking"""

    orientation: t.Optional[str]
    """The orientation of the PV modules within their racking.

    - Possible values: "portrait" (length is vertical) or "landscape" (width is vertical)
    - Default is "portrait"
    """
    vertical: t.Optional[int]
    """The number of modules along the vertical axis (side) of the racking table.

    - Default value is 2
    """
    horizontal: t.Optional[int]
    """The number of modules along the horizontal axis (bottom) of the racking table per sub-array.

    - Default value is 48
    """
    aspect_ratio: t.Optional[float]
    """The ratio of the module length to module width.

    - Default value is 1.7
    """

    @root_validator(skip_on_failure=True)
    def all_or_none(cls, values):
        missing = [v is None for k, v in values.items()]
        assert all(missing) or not any(missing), "Either all or no attributes must be assigned in Layout"
        return values


class Transformer(BaseModel):
    """Inputs for modeling transformers (both high (HV) and medium voltage (MV))"""

    rating: t.Optional[float]
    """The transformer’s rated power capacity
    
    - Units: kW
    - Example value: 100000.0
    """
    load_loss: float
    """The transformer’s load-dependent loss factor (coil losses) when operating at the rated capacity

    - Units: unitless
    - Recommended values:
       - HV transformer/GSU = 0.007
       - MV transformer = 0.009
    
    """
    no_load_loss: float
    """The transformer's constant loss factor (core losses)

    - Units: unitless
    - Recommended values:
       - HV transformer/GSU = 0.002
       - MV transformer = 0.001
    """


class ACLosses(BaseModel):
    """Inputs related to system losses that occur downstream of the solar/BESS inverters"""

    ac_wiring: float = 0.01
    """Losses from MV AC wiring resistance between the inverter/MV transformer and the point of interconnection (or
    HV transformer if applicable).

    - Units: fraction
    """
    transmission: float = 0.0
    """Losses from HV AC wiring resistance, i.e. gen-tie wiring losses.

    - Units: fraction
    """
    # Feeds into nrel_sam.AdjustmentFactors rather than nrel_sam.Losses
    poi_adjustment: float = 0.0  # TODO: deprecate this?
    """Adjust AC power at POI to account for additional arbitrary losses. For example, use this input to apply a
    constant haircut to model system availability

    - Negative values can be used to represent power gains
    - Units: fraction
    """
    transformer_load: t.Optional[float]  # deprecate
    """Deprecated. Please use :attr:`hv_transformer`.
    
    `The high-voltage transformer's load-dependent loss factor (coil losses)`
    """
    transformer_no_load: t.Optional[float]  # deprecate
    """Deprecated. Please use :attr:`hv_transformer`.
    
    `The high-voltage transformer's constant loss factor (core losses)`
    """
    hv_transformer: t.Optional[Transformer]
    """Inputs for modeling a HV transformer/GSU. Setting to ``None`` assumes the system interconnection voltage is such
    that a GSU is not needed. For parameter recommendations, see :class:`Transformer`
    """
    mv_transformer: t.Optional[Transformer]
    """Inputs for modeling a MV transformer. If the inverter model given in the ``inverter`` attribute of
    :class:`PVGenerationModel`, :class:`DCExternalGenerationModel` or :class:`DownstreamSystem` includes MV transformer
    effects, then this should be set to ``None`` to avoid double-counting losses. Otherwise, a :class:`Transformer`
    object should be provided to ensure transformer losses are accounted for. For parameter recommendations,
    see :class:`Transformer`
    """

    @root_validator(skip_on_failure=True)
    def check_repeated_hv_transformer(cls, values):
        assert (values["transformer_load"] is None and values["transformer_no_load"] is None) or values[
            "hv_transformer"
        ] is None, "Cannot provide hv_transformer if transformer_load or transformer_no_load are provided"
        return values


class DCLosses(BaseModel):
    """Inputs related to PV array losses that occur upstream of the solar inverters. For use (via :class:`Losses`) with
    :class:`PVGenerationModel`
    """

    dc_optimizer: float = 0.0
    """Losses from power equipment within the array, including DC optimizers and DC-DC converters.

    - Units: fraction
    - Max value: 0.2
    """
    enable_snow_model: bool = False
    """Indicates whether NREL SAM's snow loss model should be activated. If ``True``,
    :attr:`~SolarResourceTimeSeries.snow` in :attr:`SolarResource.data` must be provided. 
    """
    dc_wiring: float = 0.02
    """Losses from DC wiring resistance within the array.

    - Units: fraction
    - Max value: 0.2
    """
    soiling: t.List[float] = Field(default_factory=lambda: 12 * [0.0])
    """Monthly reduction in irradiance occurring from dust, dirt, or other substances on the surface of the module.
    If :attr:`enable_snow_model` is ``False``, this input should also be used to account for any snow losses.

    - Units: fraction
    - Format as a list of 12 floats representing the decimal value of loss
    - Max value for each month: 0.2
    """
    diodes_connections: float = 0.005
    """Losses from voltage drops of diodes and electrical connections.

    - Units: fraction
    - Max value: 0.2
    """
    mismatch: float = 0.01
    """Losses due to differences in the max power point of individual modules, as well as differences between
    strings. These differences can be due to manufacturing variation as well as varied shading across the array.

    - Units: fraction
    - Max value: 0.2
    """
    nameplate: float = 0.0
    """Deviations between the nameplate rating provided by a manufacturer and actual/tested performance. This input
    could be used to represent positive binning tolerance or the situation where you need to model a PV module with a
    different wattage than the one you have model parameters for.

    - Units: fraction
    - Positive values represent a loss, negative values represent a gain
    - Example: A module with 405W nameplate power and +5W binning tolerance could be represented by a 400W module model
      and :math:`nameplate = 1 - (1 + 0.05/2)(405/400) = -0.0378`
    """
    rear_irradiance: float = 0.0
    """Losses associated with irradiance on the back surface of bifacial modules. Should be 0.0 for monofacial
    modules. This would include the effects of rearside rack-shading, soiling, and mismatch

    - Units: fraction
    """
    mppt_error: float = 0.0  # TODO: remove once mppt_error deprecated, equivalent to tracking_error
    """Deprecated (as well as misnamed). Use :attr:`tracking_error` instead
    """
    tracking_error: float = 0.0
    """Losses due to tracking system error in single-axis tracking systems. Should be 0.0 for fixed tilt systems.
    
    - Units: fraction
    """
    # Feeds into nrel_sam.AdjustmentFactors rather than nrel_sam.Losses
    lid: float = 0.0
    """Losses due to Light- and elevated Temperature-Induced Degradation.

    - Units: fraction
    """
    dc_array_adjustment: float = 0.0
    """Adjust DC power at inverter input to account for additional arbitrary losses or gains.

    - Negative values can be used to represent power gains
    - Units: fraction
    """

    @root_validator(skip_on_failure=True)
    def check_tracker_losses(cls, values):  # TODO: remove once mppt_error deprecated, equivalent to tracking_error
        assert (
            values["mppt_error"] * values["tracking_error"] == 0.0
        ), "Only one of mppt_error and tracking_error may be nonzero"
        return values


class Losses(ACLosses, DCLosses):
    """Container class that combines :class:`ACLosses` and :class:`DCLosses` for use with :class:`PVGenerationModel`"""

    class Config:
        extra = "forbid"


class DCProductionProfile(BaseModel):
    """Time series inputs associated with a DC generation source (e.g. PV array). For use with
    :class:`DCExternalGenerationModel`
    """

    power: t.List[float]
    """The net power at all DC-DC busbars for DC-Coupled systems, or all inverter MPP inputs for solar-only
    systems. This power will be divided by the number of inverters determined based on
    :attr:`DCExternalGenerationModel.inverter` and the system AC capacity before being passed through the inverter
    model in :attr:`DCExternalGenerationModel.inverter`

    - Should not consider any inverter clipping effects on DC power (since this clipping could be captured by a
      DC-coupled BESS and will be modeled in the inverter model anyways)
    - Assumed to include any aging/degradation effects
    - In PVSyst, this field is EArrayMPP (not EArray), though PVsyst does not consider degradation
    - Units: kW
    - Example: For a nameplate 100MWdc array at STC for 3 hours, the input would be [100000, 100000, 100000].
    """
    voltage: t.List[float]
    """The voltage at the DC-DC busbar for DC-Coupled systems or inverter MPP input for solar-only systems. Unlike
    :attr:`power`, total array voltage is not the sum of inverter DC voltages, so these values will not be divided
    before being passed into the inverter model.

    - In PVSyst, this field is Uarray
    - Units: V
    - Example: For a nominal 1500Vdc system, the max values should be somewhere near but below 1500V.
    """
    ambient_temp: t.Optional[t.List[float]]
    """Hourly ambient temperature. Used for inverter efficiency and HVAC model (when used).
    
    - Units: - Units: |degrees|\ C
    - Example values: [25.0, 35.0, 45.0]
    """

    @root_validator(skip_on_failure=True)
    def check_length(cls, values):
        _check_lengths({"power": values["power"], "voltage": values["voltage"]})
        if values["ambient_temp"]:
            _check_lengths({"power": values["power"], "ambient_temp": values["ambient_temp"]})
        return values

    def __len__(self) -> int:
        return len(self.power)


class ACProductionProfile(BaseModel):
    """Time series inputs associated with an MV AC generation source (e.g. PV MV output, wind turbines etc.). For use
    with :class:`ACExternalGenerationModel`
    """

    power: t.List[float]
    """The power at the MV AC bus (i.e. where a MV BESS system would tie-in) 

    - In PVSyst, this field is EOutInv if inverter modeling takes into account MV transformer losses. If not,
      use E_Grid with all models downstream of the mv transformer turned off or set to zero
    - Units: kW
    """
    ambient_temp: t.Optional[t.List[float]]
    """Hourly ambient temperature. Used for HVAC model if applicable.

    - Units: - Units: |degrees|\ C
    - Example values: [25.0, 35.0, 45.0]
    """

    # if ACProductionProfile is allowed to have extra fields in the payload, then a DCProductionProfile payload will be
    # coerced into an ACProductionProfile object if something is wrong with voltage
    class Config:
        extra = "forbid"

    @root_validator(skip_on_failure=True)
    def check_length(cls, values):
        if values["ambient_temp"]:
            _check_lengths({"power": values["power"], "ambient_temp": values["ambient_temp"]})
        return values

    def __len__(self) -> int:
        return len(self.power)


ProductionProfile = t.Union[DCProductionProfile, ACProductionProfile]


class BaseSystemDesign(BaseModel):
    """Base class for system design objects"""

    dc_capacity: float
    """The total nameplate DC capacity of all the modules in a system.

    - Units: kWdc
    - Example: 1000.0 for a 1000 kWdc system
    """
    ac_capacity: float
    """The total nameplate AC capacity of all the inverters in a system.

    - Units: kWac
    - Example: 1000.0 for a 1,000 kWac system
    """
    poi_limit: float
    """The maximum injection capacity at the point of interconnection (usually defined by an interconnection
    agreement).

    - Units: kWac
    - Example: 1000.0 for a system with 1MW in interconnection capacity
    """


@optional_discriminators(["tracking"])
class PVSystemDesign(BaseSystemDesign):
    """Inputs for PV wiring and array configuration. A submodel for :attr:`PVGenerationModel.system_design`"""

    modules_per_string: t.Optional[int]
    """The number of modules connected in series for a single string. Generally Dependent on inverter and module
    selection. If not provided, a string size that keeps voltage within the inverter MPPT range is selected as part of
    the simulation.
    """
    strings_in_parallel: t.Optional[int]
    """The number of module strings connected in parallel to form an array. Generally dependent on `dc_capacity` and
    module selection. If not provided, Tyba will make an assumption as part of the simulation.
    """
    tracking: t.Union[FixedTilt, SingleAxisTracking] = Field(..., discriminator="tracking_type")
    """A sub-model to represent the PV racking design"""
    azimuth: t.Optional[float]
    """Orientation of the array towards the sun. Note that for fixed tilt systems, this means the direction in which
    the modules are tilted, whereas for single-axis tracking systems this means the direction of the axis of
    clock-wise rotation

    - Units: degrees east of north, with due north having a value of 0.0
    - Default value is 180\ |degrees| (due south) for the northern hemisphere and 0\ |degrees| (due north) for the
      southern hemisphere
    - Fixed Tilt Example: A northern hemisphere system with an azimuth of 190\ |degrees|
      would have all of its modules titled to face 10\ |degrees| west of due south
    - Single Axis Tracking Example: In the northern hemisphere, an azimuth of 180\ |degrees| (the default), would have
      the system tilted towards due east in the morning and due west in the evening. An azimuth of 190\ |degrees| would
      have the modules facing slightly south of east in the morning and slightly north of west in the evening 
    """
    gcr: float
    """The ratio of total module area to total land area. This is a measure of inter-row spacing, where a low
    ratio means the rows are more spread out and a higher ratio means the rows are tightly packed. Note that the tilt
    in fixed tilt systems is not to be taken into account (not a projected area in the numerator).

    - Example: 0.33
    """


class TermUnits(str, Enum):
    """Enum for indicating project term units"""

    hours = "hours"
    """Project term value is in units of hours"""
    days = "days"
    """Project term value is in units of days"""
    years = "years"
    """Project term value is in units of years"""


class ProjectTermMixin(BaseModel):
    """Mixin class used to add project term inputs to simulation classes"""

    project_term: int = 1
    """Integer value with units given by :attr:`project_term_units` that defines the project term (timespan) to be
    simulated.
    
    - For typical-year hybrid and solar-only simulations, the year-long time series in
      :attr:`PVGenerationModel.solar_resource` will be tiled to match :attr:`project_term`. As such, the project term
      must represent a number of whole years
    - For all other hybrid and solar-only simulations, the project term must match the timespan represented by
      :attr:`BaseGenerationModel.time_interval_mins` and the length of the corresponding solar resource or power time
      series
    - For standalone storage simulations, the project term must match the timespan represented by
      :attr:`StandaloneStorageModel.time_interval_mins` and the corresponding price time series
    """
    project_term_units: TermUnits = "years"
    """Units to be applied to :attr:`project_term` to define the term (timespan) to be simulated. See
    :attr:`project_term` for constraints
    
    """


class BaseGenerationModel(ProjectTermMixin):
    """Base class for generation model classes"""

    project_type: t.Optional[t.Literal["generation"]] = "generation"
    """Used by the API for model-type discrimination, can be ignored"""
    time_interval_mins: int = 60
    """Time interval that corresponds to time series in :attr:`PVGenerationModel.solar_resource` or
    :attr:`ExternalGenerationModel.production_override`
    
    - Units: minutes
    """


def scale_project_term_to_hours(project_term: int, project_term_units: TermUnits) -> int:
    """:meta private:"""
    if project_term_units == "hours":
        return project_term
    elif project_term_units == "days":
        return 24 * project_term
    else:  # years
        return 8760 * project_term


def _check_time_interval_project_term(
    signal_len, signal_str, project_term, time_interval_mins, project_term_units: TermUnits
):
    """
    For more on why we treat project_term as an int and validate like we do check out this PR comment:
    https://github.com/Tyba-Energy/generation/pull/186#discussion_r1054578658. The broader PR has even more context
    should it be needed
    """
    signal_hours = int(signal_len * (time_interval_mins / 60))
    project_term_hours = scale_project_term_to_hours(project_term, project_term_units)
    assert project_term_hours == signal_hours, (
        f"project_term, project_term_units, time_interval_mins, and length of {signal_str} must be consistent; "
        f"got {project_term}, {project_term_units}, {time_interval_mins}, and {signal_len} respectively"
    )


class ExternalGenerationModel(BaseGenerationModel):
    """Base class for classes that represent AC or DC external generation sources"""

    losses: t.Union[ACLosses, Losses]
    """Submodel for losses that occur downstream of the bus associated with :attr:`production_override`
    """
    production_override: ProductionProfile
    """Submodel for time series (power etc) generated by external generation source
    """
    system_design: BaseSystemDesign
    """Submodel that defines system size for reporting, inverter sizing, and POI limiting
    """

    @root_validator(skip_on_failure=True)
    def check_time_interval_project_term(cls, values):
        _check_time_interval_project_term(
            len(values["production_override"]),
            "production_override",
            values["project_term"],
            values["time_interval_mins"],
            values["project_term_units"],
        )
        return values

    def __len__(self) -> int:
        return len(self.production_override)


class Bus(str, Enum):
    """Enum class for selecting coupling bus for hybrid systems"""

    DC = "DC"
    """indicates the BESS and generator are coupled together at the DC inputs of the generator inverter"""
    MV = "MV"
    """indicates the BESS and generator are coupled at the medium voltage AC bus"""
    HV = "HV"
    """indicates the BESS and generator are coupled at the high voltage AC bus, e.g. the outlet of the GSU/substation"""


class DownstreamSystem(BaseModel):
    """Submodel for detailed treatment of losses in standalone storage systems that aren't already considered as
    part of :attr:`~BatteryParams.charge_efficiency` and :attr:`~BatteryParams.discharge_efficiency`
    """

    losses: ACLosses  # still only ACLosses if modeling from inverter input, since almost every DC loss pertains to PV.
    """Submodel for post-inverter losses to be considered. Note that, depending on the coupling bus specified by
    :attr:`model_losses_from`, some of the attributes of :class:`ACLosses` will be ignored. For example, if the
    coupling bus is specified as high voltage, :attr:`ac_wiring` and :attr:`mv_transformer` will be ignored, since
    they are upstream of the coupling bus.
    """
    system_design: BaseSystemDesign
    """Submodel that defines system size for reporting, inverter sizing, and POI limiting
    """
    model_losses_from: Bus
    """Indicates the coupling bus downstream of which detailed loss modeling should occur. All losses/effects upstream
    of this bus are assumed to be rolled into :attr:`BatteryParams.charge_efficiency` and
    :attr:`BatteryParams.discharge_efficiency`
    """
    inverter: t.Optional[InverterTypes]
    """Submodel for inverter used in system design. Required if :attr:`model_losses_from` is "DC", otherwise ignored"""

    @root_validator(skip_on_failure=True)
    def inverter_only_if_dc(cls, values):
        if values["inverter"] is not None:
            assert values["model_losses_from"] == Bus.DC, "model_losses_from must be 'DC' if inverter is provided"
        return values


class ACExternalGenerationModel(ExternalGenerationModel):
    """Inputs specifying a MV AC generation source, e.g. PV MV power from a non-Tyba source, wind power, etc. Intended
    to be passed into :attr:`PVStorageModel.pv_inputs` for hybrid simulations but can also be used as a simulation
    class for generation-only simulations
    """

    generation_type: t.Optional[t.Literal["ExternalAC"]] = "ExternalAC"
    """Used by the API for model-type discrimination, can be ignored"""
    losses: ACLosses = ACLosses()
    """Submodel for system losses. :attr:`ACLosses.mv_transformer` must be ``None`` since the
    :attr:`production_override` is assumed to be at medium voltage already.
    """
    production_override: ACProductionProfile
    """Submodel for time series related to generator power. Assumed to be power at the MV AC bus"""

    @validator("losses")
    def no_mv_xfmr(cls, v: ACLosses):
        assert v.mv_transformer is None, (
            "losses.mv_transformer must be None, since the production_override provided in "
            "an ACExternalGenerationModel is assumed to be at the MV bus"
        )
        return v


class DCExternalGenerationModel(ExternalGenerationModel):
    """Inputs for specifying a DC generation source, e.g. PV array power from a non-Tyba source. Intended
    to be passed into :attr:`PVStorageModel.pv_inputs` for hybrid simulations but can also be used as a simulation
    class for generation-only simulations.
    """

    generation_type: t.Optional[t.Literal["ExternalDC"]] = "ExternalDC"
    """Used by the API for model-type discrimination, can be ignored"""
    losses: Losses = Losses()
    """Submodel for system losses"""
    production_override: DCProductionProfile
    """Submodel for time series related to generator power.
    
    - Assumed to be at DC bus/inverter MPPT inputs
    - Assumed to include any aging/degradation effects
    """
    inverter: InverterTypes
    """Submodel for inverter to be used with generation source"""


class ArrayDegradationMode(str, Enum):
    """Enum for specifying the PV array degradation approach to be used in a :class:`PVGenerationModel` or
    :class:`PVStorageModel` simulation
    """

    linear = "linear"
    """The degradation applied to each year of PV DC generation will increase linearly. The annual degradation derate
    is calculated as :math:`1-r_{degrad}*n_{year}` where :math:`r_{degrad}` is the degradation rate specified by
    :attr:`PVGenerationModel.array_degradation_rate` and :math:`n_{year}` is the count for the year in question.
    
    - Example: For a degradation rate of 0.005 (0.5%), the degradation derate applied to all time intervals of year 1 is
      :math:`1-0.005*1=0.995`
    """
    compounding = "compounding"
    """The degradation applied to each year of PV DC generation will be compounding. The degradation derate is
    calculated as :math:`(1-r_{degrad})^{n_{year}}` where :math:`r_{degrad}` is the degradation rate
    specified by :attr:`PVGenerationModel.array_degradation_rate` and :math:`n_{year}` is the count for the year
    in question.
    
    - Example: For a degradation rate of 0.005 (0.5%), the degradation derate applied to all time intervals of year 2 is
      :math:`(1-0.005)^2=0.99`
    """


def solar_resource_is_typical(solar_resource, time_interval_mins, project_term, project_term_units) -> bool:
    if isinstance(solar_resource, (tuple, SolarResourceLocation)):
        return True
    if (
        isinstance(solar_resource, SolarResource)
        and (int(len(solar_resource) * time_interval_mins / 60) == 8760)
        and (scale_project_term_to_hours(project_term, project_term_units) % 8760 == 0)
        and (scale_project_term_to_hours(project_term, project_term_units) >= 8760)
    ):
        return True
    return False


def _pv_gen_len(solar_resource, time_interval_mins, project_term, project_term_units) -> int:
    if isinstance(solar_resource, SolarResource):
        if solar_resource_is_typical(solar_resource, time_interval_mins, project_term, project_term_units):
            return len(solar_resource) * int(scale_project_term_to_hours(project_term, project_term_units) / 8760)
        return len(solar_resource)
    return 8760 * int(scale_project_term_to_hours(project_term, project_term_units) / 8760)


class PVGenerationModel(BaseGenerationModel):
    """Simulation class for solar-only simulations, or can be passed into :attr:`PVStorageModel.pv_inputs` for
    hybrid simulations"""

    generation_type: t.Optional[t.Literal["PV"]] = "PV"
    """Used by the API for model-type discrimination, can be ignored"""
    solar_resource: t.Union[SolarResource, t.Tuple[float, float], SolarResourceLocation]
    """Input for irradiance and weather time series and location information. Can take multiple argument types:
    
    - A :class:`SolarResource` object for full specification of solar resource. Must be used if resource does *not*
      represent a Typical Year (TY), but can also represent a TY. See :class:`SolarResourceTimeSeries` for more info.
    - A :class:`SolarResourceLocation` object. With this type, Tyba will pull TY solar resource data from
      the `NSRDB <https://nsrdb.nrel.gov/>`__ and use it in the simulation
    - A tuple of (latitude, longitude) where the values are in decimal degrees. This argument is
      equivalent to passing a :class:`SolarResourceLocation` object with ``region="North America"``
      
    Tiling of solar resource data to match the :attr:`project_term` is only supported for TY data
    """
    inverter: InverterTypes
    """Inputs for inverter submodel. Can take multiple argument types:
    
    - An :class:`Inverter` or :class:`ONDInverter` object for full specification of the inverter model. In particular,
      use this type (along with :func:`tyba_client.io.inverter_from_ond`) if you are trying to model an inverter from 
      a local OND file
    - A string of the exact inverter name in Tyba's default inverter inventory (as shown in the web application)
    - A :class:`FileComponent` object that specifies the exact path of an OND file that was previously uploaded to
      Tyba via the web application
    """
    pv_module: PVModuleTypes
    """Inputs for PV module/array submodel. Can take multiple argument types:
    
    - An :class:`PVModuleCEC` or :class:`PVModuleMermoudLejeune` object for full specification of the PV module model.
      In particular, use this type (along with :func:`tyba_client.io.pv_module_from_pan`) if you are trying to model
      a PV module from a local PAN file
    - A string of the exact PV module name in Tyba's default module inventory (as shown in the web application)
    - A :class:`FileComponent` object that specifies the exact path of a PAN file that was previously uploaded to
      Tyba via the web application"""
    layout: Layout = Layout()
    """Inputs that describe module/racking geometry"""
    losses: Losses = Losses()
    """Submodel for both array and AC-side losses"""
    system_design: PVSystemDesign
    """Inputs for system size and geometry"""
    array_degradation_rate: float = 0.005
    """Degradation rate applied annually to pre-inverter array DC power as specified by the
    :attr:`array_degradation_mode`. Ignored if :attr:`solar_resource` does not represent a Typical Year
    """
    array_degradation_mode: t.Optional[ArrayDegradationMode] = ArrayDegradationMode.linear
    """Method by which to apply :attr:`array_degradation_rate` to pre-inverter array DC power.
    
    - If ``None``, no degradation will be modeled
    - Only applicable if :attr:`solar_resource` represents a Typical Year, otherwise must be ``None``
    """

    def __len__(self) -> int:
        return _pv_gen_len(self.solar_resource, self.time_interval_mins, self.project_term, self.project_term_units)

    @root_validator(skip_on_failure=True)
    def check_data_start_if_typical(cls, values):
        if isinstance(values["solar_resource"], SolarResource) and solar_resource_is_typical(
            values["solar_resource"], values["time_interval_mins"], values["project_term"], values["project_term_units"]
        ):
            assert (
                values["solar_resource"].data.month[0],
                values["solar_resource"].data.day[0],
                values["solar_resource"].data.hour[0],
            ) == (
                1,
                1,
                0,
            ), "solar resource data must start at Jan 1, hour 0 when typical solar resource is provided"
        return values

    @root_validator(skip_on_failure=True)
    def check_time_interval_project_term(cls, values):
        _check_time_interval_project_term(
            _pv_gen_len(
                values["solar_resource"],
                values["time_interval_mins"],
                values["project_term"],
                values["project_term_units"],
            ),
            "solar_resource",
            values["project_term"],
            values["time_interval_mins"],
            values["project_term_units"],
        )
        return values

    @root_validator(skip_on_failure=True)
    def check_degradation_mode_for_nontypical(cls, values):
        if not solar_resource_is_typical(
            values["solar_resource"], values["time_interval_mins"], values["project_term"], values["project_term_units"]
        ):
            assert (
                values["array_degradation_mode"] != "linear"
            ), "Linear PV array degradation not currently supported for non-typical year simulations"
        return values

    @root_validator(skip_on_failure=True)
    def default_azimuth_from_location(cls, values):
        system_design: PVSystemDesign = values["system_design"]
        solar_resource = values["solar_resource"]
        if system_design.azimuth is None:
            if isinstance(solar_resource, tuple):
                system_design.azimuth = 180.0 if solar_resource[0] >= 0.0 else 0.0
            elif isinstance(solar_resource, (SolarResource, SolarResourceLocation)):
                system_design.azimuth = 180.0 if solar_resource.latitude >= 0.0 else 0.0
            else:
                raise NotImplementedError("No default azimuth handling for this solar resource model")
        return values


GenerationModel = Annotated[
    t.Union[PVGenerationModel, DCExternalGenerationModel, ACExternalGenerationModel],
    Field(discriminator="generation_type"),
]


class TableCapDegradationModel(BaseModel):
    """Submodel for defining BESS energy capacity degradation as a table of values. Intended as a way to bring data in
    from a guaranteed capacity table included in a BESS purchase order/warranty. Note that although this model
    applies degradation based on time passing, it can account for both cycle and calendar degradation assuming the
    guaranteed cap table specifies an annual cycle count and this is similar to the annual cycle counts in the
    simulation
    """

    annual_capacity_derates: t.List[float]
    """List of end-of-year BESS energy capacity derates relative to initial BESS capacity, starting with year 0. At
    the end of each solver step as defined by :attr:`StorageSolverOptions.step`, the BESS capacity will be reduced
    based on time passed such that the capacity matches the list derate at the end of each simulation year.
    
    - First value in the list must be 1.0 (year 0 has no degradation)
    - Example: For annual derates [1.0, .9915, 0.9856] and an initial capacity of 100MWh, energy capacity will decrease
      linearly in a step-wise fashion until it is :math:`100*0.9915=99.15MWh` at the end of year 1 and
      :math:`100*0.9856=98.56MWh` at the end of year 2.
    - List length must be greater than or equal to :attr:`BatteryParams.term`
    """


class TableEffDegradationModel(BaseModel):
    """Submodel for defining BESS efficiency degradation as a table of values. Intended as a way to bring data in
    from a BESS purchase order/warranty. Note that although this model applies degradation based on time passing, it
    can account for both cycle and calendar degradation assuming the PO/warranty specifies an annual cycle count and
    this is similar to the annual cycle counts in the simulation
    """

    annual_efficiency_derates: t.List[float]
    """List of end-of-year BESS efficiency derates relative to initial BESS charge and discharge efficiency, starting
    with year 0. At the end of each solver step as defined by :attr:`StorageSolverOptions.step`, the BESS efficiency
    parameters will be reduced based on time passed such that the efficiency matches the list derate at the end of
    each simulation year.

    - First value in the list must be 1.0 (year 0 has no degradation)
    - Example: For annual derates [1.0, .9915, 0.9856] and an initial charge efficiency of 98.5%, efficiency will
      decrease linearly in a step-wise fashion until it is :math:`.985*0.9915=97.66\\%` at the end of year 1 and
      :math:`0.985*0.9856=97.08\\%` at the end of year 2.
    - List length must be greater than or equal to :attr:`BatteryParams.term`
    """


class BatteryHVACParams(BaseModel):
    """Submodel for more detailed estimation of BESS HVAC losses. Requires ambient temperature time series as a
    simulation input"""

    container_temperature: float
    """Target temperature that BESS container is assumed to be maintained at
    
    - Units: |degrees|\ C
    - Example value: 25\ |degrees|\ C
    """
    cop: float
    """The HVAC’s coefficient of performance.

    - Example value: 3.0
    """
    u_ambient: float
    """The heat transfer coefficient between ambient and the container

    - Units: W/Km\ :sup:`2`
    - Example value: 100.0W/Km\ :sup:`2`
    """
    discharge_efficiency_container: float
    """The portion of the BESS’s discharge efficiency driven by losses within the battery container, i.e., cell, rack
    and BMS losses.
    
    - Must be a greater than :attr:`~BatteryParams.discharge_efficiency`.
    - Units: fraction
    - Example value: 0.98
    """
    charge_efficiency_container: float
    """The portion of the BESS’s charge efficiency driven by losses within the battery container, i.e., cell, rack and
    BMS losses.
    
    - Must be greater than :attr:`~BatteryParams.charge_efficiency`
    - Units: fraction
    - Example value: 0.98
    """
    aux_xfmr_efficiency: float
    """The efficiency of the transformer stepping down from medium voltage to the voltage of the HVAC system.

    - Units: fraction
    - Example value: 0.99
    """
    container_surface_area: float = 20.0
    """Surface area of a single BESS container over which it exchanges heat with the ambient. Generally should
    consider area in contact with the ground, depending on how :attr:`u_ambient` has been determined
    
    - Units: m\ :sup:`2`
    - Example value: 20.0 
    """
    design_energy_per_container: float = 750.0
    """Design energy capacity per each BESS container. Used to estimate the number of containers in the BESS, and
    (along with :attr:`container_surface_area`) the corresponding total surface area available for heat transfer
    
    - Units: kWh
    - Example value: 750.0kWh
    """


class BatteryParams(BaseModel):
    """Inputs for modeling the physical performance of a BESS"""

    power_capacity: float
    """The maximum usable capacity of the battery to draw power to charge. Assumed to be equivalent for charge and
    discharge. For hybrid simulations, represents maximum power at coupling bus. For standalone storage simulations,
    represents maximum power at the point of interconnection or at the bus specified in
    :attr:`DownstreamSystem.model_losses_from` if applicable
    
    - Units: kW
    - Example value: 1000kW 
    """
    energy_capacity: float
    """The maximum usable capacity of the battery to store energy.
    
    - Units: kWh
    - Example value: 2000kWh
    """
    charge_efficiency: float
    """The percentage of energy stored for every kW of power drawn to charge. For hybrid simulations, should account
    for all losses up to the coupling bus. For standalone storage simulations, should account for all losses up to the
    point of interconnection or all losses up to the bus specified in :attr:`DownstreamSystem.model_losses_from`. If
    :attr:`hvac` is defined, *should not* account for BESS HVAC load.
    
    - Units: fraction
    - Example value: 0.965
    """
    discharge_efficiency: float
    """The percentage of energy discharged for every kW of power drawn to discharge. For hybrid simulations, should
    account for all losses up to the coupling bus. For standalone storage simulations, should account for all losses
    up to the point of interconnection or all losses up to the bus specified in
    :attr:`DownstreamSystem.model_losses_from`. If :attr:`hvac` is defined, *should not* account for BESS HVAC load.
    
    - Units: fraction
    - Example value: 0.965
    """
    self_discharge_rate: t.Optional[float]
    """Ratio of self-discharge power to SOE, applied when the battery is idle. If a value is provided, self-discharge is
    calculated like: ``self_discharge_rate * SOE``. If ``None``, no self-discharge occurs.
    
    - Units: kW/kWh
    - Example value: 0.01
    """
    degradation_rate: t.Optional[float]
    """The approximate year over year (YoY) decrease in storage energy capacity due to cycling. Even though it is a YoY
    value, this specifies a throughput degradation model, meaning the battery degrades this percentage every
    :attr:`degradation_annual_cycles` cycles. At the end of each solver step as defined by
    :attr:`StorageSolverOptions.step`, the BESS capacity will be reduced
    based on the number of cycles that have occurred.
    
    - Either this parameter or :attr:`capacity_degradation_model` must be specified. To model no degradation, simply
      set to 0.0
    - Units: fraction
    - Example: for a ``degradation_rate`` of 1% and ``degradation_annual_cycles`` of 261, a simulation step where 2.5
      cycles occur will reduce the BESS capacity by :math:`(0.01/261)*2.5=0.00958\\%`
    """
    degradation_annual_cycles: float = 261  # cycle / work day
    """Assumed number of annual cycles corresponding to :attr:`degradation_rate`. See :attr:`degradation_rate` for more
    details"""
    hvac: t.Optional[BatteryHVACParams]
    """Submodel for more accurately modeling the efficiency of a BESS as a function of temperature.
    
    - Requires ambient temperature as a simulation input
    - If ``None``, HVAC losses should be accounted for in :attr:`charge_efficiency` and :attr:`discharge_efficiency`
    """
    capacity_degradation_model: t.Optional[TableCapDegradationModel]
    """Specification of the storage energy capacity degradation model. This can be used as an alternative to
    :attr:`degradation_rate` and :attr:`degradation_annual_cycles`. Currently, only models of type
    :class:`TableCapDegradationModel` are supported.
    
    - Either this parameter or :attr:`degradation_rate` must be specified. To model no degradation, use
      :attr:`degradation_rate` and set to 0.0
    - If specified, must include enough data to cover the battery :attr:`term`
    """
    efficiency_degradation_model: t.Optional[TableEffDegradationModel]
    """Specification of the storage charge and discharge efficiency degradation model. Current, only models of type
    TableEffDegradationModel are supported. If ``None``, no efficiency degradation is modeled
    
    - If specified, must include enough data to cover the battery :attr:`term`
    """
    term: t.Optional[float]
    """The number of years this specific battery will be active.

    - When multiple batteries are given in :attr:`MultiStorageInputs.batteries`, this parameter is required and used to
      specify replacement/augmentation
    - In this case, the total of all battery terms needs to match the timespan of :attr:`MarketBase.energy_prices`
    - Only optional if a single battery is specified in :attr:`MultiStorageInputs.batteries`. In this case the term is
      assumed to be equivalent to the project term
    """

    @root_validator(skip_on_failure=True)
    def check_cap_degradation_models(cls, values):
        assert not (
            values["degradation_rate"] is None and values["capacity_degradation_model"] is None
        ), "Either degradation_rate or capacity_degradation_model must be specified"
        assert (
            values["degradation_rate"] is None or values["capacity_degradation_model"] is None
        ), "Only one of degradation_rate and capacity_degradation_model may be specified"
        return values

    @root_validator(skip_on_failure=True)
    def check_degrad_table_length(cls, values):
        term = values["term"] or 0  # validate against term if term is provided
        for dm in "capacity", "efficiency":
            if values[f"{dm}_degradation_model"]:
                assert (
                    len(getattr(values[f"{dm}_degradation_model"], f"annual_{dm}_derates")) - 1 >= term
                ), f"annual_{dm}_derates must be long enough to cover battery term"
        return values


class EnergyStrategy(str, Enum):
    """Enum for specifying energy market participation strategy"""

    da = "DA"
    """Make quantity-only bids into the day-ahead market and do not bid into the real-time market. Real-time
    participation will only cover day-ahead bids, but resource is still exposed to real-time prices if participating in
    ancillary/reserve markets with non-zero utilization
    """
    rt = "RT"
    """Make quantity-only bids into real-time market and do not bid into the day-ahead market
    """
    dart = "DART"
    """Make quantity-only bids into both the day-ahead and real-time markets
    """

    def to_market_config(self) -> MarketConfig:
        return {
            "DA": MarketConfig(da=BidOfferStrategy.quantity_only, rt=None),
            "RT": MarketConfig(da=None, rt=BidOfferStrategy.quantity_only),
            "DART": MarketConfig(da=BidOfferStrategy.quantity_only, rt=BidOfferStrategy.quantity_only),
        }[self]


class BidOfferStrategy(str, Enum):
    """:meta private:"""

    quantity_only = "quantity-only"
    price_quantity = "price-quantity"
    awarded = "awarded"


class MarketConfig(BaseModel):
    """:meta private:"""

    da: t.Optional[BidOfferStrategy]
    rt: t.Optional[BidOfferStrategy]

    @validator("rt")
    def valid_rt_configs(cls, v):
        if v not in {BidOfferStrategy.quantity_only, None}:
            raise ValueError("only quantity-only supported for RTM")
        return v

    @property
    def independent_dam(self) -> bool:
        return self.da is not None and self.rt is not None

    @property
    def value(self) -> str:
        """For symmetry with EnergyStrategy"""
        return json.dumps({"DAM": self.da.value, "RTM": self.rt.value})


default_market_config = MarketConfig(
    da=BidOfferStrategy.quantity_only,
    rt=None,
)


class BoundedFloat(BaseModel):
    """:meta private:"""

    actual: float
    min: float
    max: float


class StorageSolverOptions(BaseModel):
    """Inputs related to BESS market participation and optimization"""

    cycling_cost_adder: float = 0.0
    """A hurdle rate to add costs in the optimization framework to reduce cycling. This value is often set at around
    the Variable O&M cost or the expected cost of degradation.

    - Units: $/MWh
    - Example value: $15/MWh
    """
    annual_cycle_limit: float = None
    """The maximum number of complete cycles per year. A cycle is measured as the throughput equivalent of the energy
    capacity fully charging and discharging. 

    - Units: N/A
    - Example value: 250
    """
    disable_intra_interval_variation: bool = True
    """:meta private:"""
    window: int = None
    """The number of time intervals that the optimization framework has knowledge of with respect to constraints. The
    optimization is rolling and optimizes for each :attr:`step` with the benefit of foresight into the broader window.

    - Default value: 24 (for a single day) for hourly runs
    """
    step: int = None
    """The number of intervals of a single optimization period.

    - For example: for the default hourly run, a step of 24 means the optimization sets charge and discharge schedules
      for a single day.
    - Default value: 24 (for a single day) for hourly runs
    """
    flexible_solar: bool = False
    """Whether or not to include solar curtailment in Ancillary Services offers. Only relevant for
    :class:`PVStorageModel` simulations

    - ``True`` will allow for solar bids into AS markets
    - ``False`` will not. Ancillary Service participation will come exclusively from the battery in this scenario.
    """
    symmetric_reg: bool = False
    """Whether or not regulation markets are symmetric. This will depend on the market you are participating in.
    
    - If ``True``, :attr:`ReserveMarkets.up` and :attr:`ReserveMarkets.down` must contain ``"reg_up"`` and
      ``"reg_down"`` items respectively. Their prices must also be equivalent.
    """
    energy_strategy: t.Optional[t.Union[EnergyStrategy, MarketConfig]]
    """Specifies energy market participation strategy
    """
    dart: t.Optional[bool]
    """Deprecated, use :attr:`energy_strategy` to specify co-optimization
    
    *Whether or not to include DA/RT co-optimization in the Energy Markets*

    - *Default value: False*
    """
    uncertain_soe: bool = True
    """Whether or not to consider SOE at the beginning of each optimization window as uncertain or not
    
    :meta private:
    """
    dam_annual_cycle_limit: float = None
    """:meta private:"""
    no_virtual_trades: bool = False
    """Whether or not virtual trades should be considered during DA/RT co-optimization
    
    - Only relevant if :attr:`energy_strategy` is :attr:`~EnergyStrategy.dart`
    - Requires that :attr:`MarketBase.energy_prices` is type :class:`DARTPrices`
    - If ``False``, real-time participation (i.e actual charge and discharge) is not required to cover day-ahead
      bids. Instead the optimizer assumes day-ahead bids can also be covered by buying energy in the real-time market.
      With perfect foresight of DA and RT prices, this approach seems highly lucrative, but doesn't reflect price
      uncertainty during actual operation and the associated level of market exposure
    - If ``True``, real-time participation is required to cover day-ahead market bids, but can participate beyond
      that. May still require real-time energy buys if participating in ancillary/reserve markets with non-zero
      utilization
    """
    # TODO: Allen to confirm ^
    initial_soe: t.Union[float, BoundedFloat] = 0.0
    """State-of-Energy of BESS at beginning of simulation as a fraction of BESS energy capacity"""
    duration_requirement_on_discharge: bool = True  # True for ERCOT
    """Whether :attr:`ReserveMarket.duration_requirement` applies to the entire reserve offer, or just the discharge
    side of the offer. ERCOT currently only constrains the discharge side. This means that if a BESS is offering to
    reduce the amount it is charging (rather than increasing the amount it is discharging) the offer will not be
    subject to the duration requirement."""
    no_stop_offers: bool = False  # just for comparing to competitors
    """:meta private:"""
    solver_config: SolverConfig = SolverConfig()
    """Inputs related to how the solution is actually carried out
    
    :meta private:
    """
    robust_range_initial_soe: bool = False
    """Interpret a BoundedFloat passed as initial_soe as a set of three different SOE scenarios to model, using the 
    "actual" scenario to compute RT revenue
    
    :meta private:
    """

    @root_validator(skip_on_failure=True)
    def coerce_strategy_to_market_config(cls, values):
        assert not (values["dart"] is not None and values["energy_strategy"] is not None), (
            "Only one of `dart` or `energy_strategy` may be provided. `dart` is deprecated; use `energy_strategy`"
            " instead."
        )
        strategy = values["energy_strategy"]
        if strategy is None:
            strategy = EnergyStrategy.dart if values["dart"] else EnergyStrategy.da
            values["dart"] = None
        if isinstance(strategy, EnergyStrategy):
            values["energy_strategy"] = strategy.to_market_config()

        if not values["energy_strategy"].independent_dam:
            if values["dam_annual_cycle_limit"] is not None:
                raise ValueError("Must model separate dam and rtm markets if dam_annual_cycle_limit is set")
            if values["no_virtual_trades"]:
                raise ValueError("Must model separate dam and rtm markets if no_virtual_trades is set to True")
        return values

    @root_validator(skip_on_failure=True)
    def check_solver_config(cls, values):
        if values["solver_config"].solver_specific and (values["solver"] not in {"HiGHS", "GLPK"}):
            raise ValueError("solver_specific options may only be passed when using HiGHS or GLPK solver")
        return values


class MultiStorageInputs(StorageSolverOptions):
    """Inputs related to BESS design, market participation and optimization"""

    batteries: t.List[BatteryParams]
    """List of ``BatteryParam`` objects that models replacement/augmentation of the BESS over a project's life.
    
    - Each :class:`BatteryParam` object is modeled for its :attr:`~BatteryParam.term` and then the BESS is assumed
      to be replaced and the SOE is assumed to be reset to :attr:`initial_soe`
    - To model a single battery over the project lifetime with no augmentation simply provide a list of length 1. In
      this case. :attr:`~BatteryParam.term` is ignored and the battery term is assumed to be equivalent to the project
      term.
    """

    @validator("batteries")
    def check_battery_terms(cls, v):
        if len(v) > 1:  # don't worry about terms if there's only one battery
            for battery in v:
                assert battery.term, "if multiple batteries are provided, terms must also be provided"
        return v


def _get_price_str_and_price(values):
    if isinstance(values["energy_prices"], DARTPrices):
        return "rtm prices", values["energy_prices"].rtm
    elif isinstance(values["energy_prices"], DARTPriceScenarios):
        return "rtm price", values["energy_prices"]
    else:
        return "energy_prices", values["energy_prices"]


class PeakWindow(BaseModel):
    """Inputs that describe peak to be reduced as part of :class:`LoadPeakReduction`

    :meta private:
    """

    # TODO: Add docs at some point for devs
    mask: t.List[bool]
    """TODO"""
    price: float
    """TODO"""


class LoadPeakReduction(BaseModel):
    """:meta private:"""

    # TODO: Add docs at some point for devs
    load: t.List[float]
    """TODO"""
    max_load: t.List[float]  # TODO: should be optional -- https://app.asana.com/0/1178990154879730/1203603348130562/f
    """TODO"""
    seasonal_peak_windows: t.List[PeakWindow] = []
    """TODO"""
    daily_peak_windows: t.List[PeakWindow] = []
    """TODO"""

    @root_validator(skip_on_failure=True)
    def check_lengths(cls, values):
        windows = [*values["seasonal_peak_windows"], *values["daily_peak_windows"]]
        assert (
            windows
        ), "One or both of seasonal_peak_windows and daily_peak_windows must be provided when using load_peak_reduction"
        length = len(values["load"])
        assert len(values["max_load"]) == length, "load and max_load must have same length"
        for window in windows:
            assert len(window.mask) == length, "peak masks must have same length as load"
        return values

    def __len__(self) -> int:
        return len(self.load)


class ImportExportLimitMixin(BaseModel):
    """Mixin class for applying import and export constraints to simulation class objects"""

    import_limit: t.Optional[t.List[float]]
    """Time series of limit values to be applied to import
    
    - Power values correspond to the time interval given by :attr:`MarketBase.time_interval_mins` and the list length
      must match RTM prices
    - All values should be <= 0
    - Units: kW
    - Example values: [-1000.0, -1000.0, 0, 0,] 
    """
    export_limit: t.Optional[t.List[float]]
    """Time series of limit values to be applied to export

    - Power values correspond to the time interval given by :attr:`MarketBase.time_interval_mins` and the list length
      must match RTM prices
    - All values should be >= 0
    - Units: kW
    - Example values: [1000.0, 1000.0, 0, 0,] 
    """

    @root_validator(skip_on_failure=True)
    def validate_limits(cls, values):
        if values["import_limit"] is not None:
            assert all([v <= 0 for v in values["import_limit"]]), "import_limit must be <= 0"
        if values["export_limit"] is not None:
            assert all([v >= 0 for v in values["export_limit"]]), "export_limit must be >= 0"
        return values

    @root_validator(skip_on_failure=True)
    def check_import_export_lengths(cls, values):
        for limit in "import_limit", "export_limit":
            if values[limit]:
                price_str, price = _get_price_str_and_price(values)
                _check_lengths({limit: values[limit], price_str: price})
        return values


def _check_degrad_table_length(values: dict):
    if len(values["storage_inputs"].batteries) == 1:
        battery = values["storage_inputs"].batteries[0]
        pt = (
            scale_project_term_to_hours(
                values.get("project_term") or values["pv_inputs"].project_term,
                values.get("project_term_units") or values["pv_inputs"].project_term_units,
            )
            / 8760
        )
        for dm in "capacity", "efficiency":
            if dm_ob := getattr(battery, f"{dm}_degradation_model"):
                tbl_yrs = len(getattr(dm_ob, f"annual_{dm}_derates")) - 1
                assert tbl_yrs >= pt, f"annual_{dm}_derates must be long enough to cover project/battery term"
    return values


def _check_symmetric_reg_inputs(values: dict):
    if values["storage_inputs"].symmetric_reg:
        assert values.get(
            "reserve_markets"
        ), "when storage_inputs.symmetric_reg is True, reserve_markets must be provided"
        assert ("reg_up" in (values["reserve_markets"].up or dict())) and (
            "reg_down" in (values["reserve_markets"].down or dict())
        ), "when storage_inputs.symmetric_reg is True, both reg_up and reg_down reg markets must be provided"

    return values


def _check_dam_award_against_config(values):
    assert (values["dam_award"] is not None) == (
        values["storage_inputs"].energy_strategy.da == BidOfferStrategy.awarded
    ), "DAM award must be provided if and only if the DAM strategy is 'awarded'"


@optional_discriminators(["pv_inputs"])
class PVStorageModel(ImportExportLimitMixin, MarketBase):
    """Simulation class for hybrid simulations"""

    project_type: t.Optional[t.Literal["hybrid"]] = "hybrid"
    """Used by the API for model-type discrimination, can be ignored"""
    storage_inputs: MultiStorageInputs
    """Submodel for BESS design, market participation and optimization"""
    storage_coupling: StorageCoupling
    """Specify the point at which the BESS and generation source are coupled"""
    pv_inputs: GenerationModel
    """Submodel for PV or external power generation"""
    enable_grid_charge_year: t.Optional[float]
    """Simulation year in which to allow grid charging. Currently, many hybrid systems are not allowed to charge from
    the grid, but are expected to be able to sometime in the future
    """

    @property
    def project_term(self) -> int:
        """Equivalent to :attr:`~ProjectTermMixin.project_term` provided in :attr:`pv_inputs`"""
        return self.pv_inputs.project_term

    @property
    def project_term_units(self) -> TermUnits:
        """Equivalent to :attr:`~ProjectTermMixin.project_term_units` provided in :attr:`pv_inputs`"""
        return self.pv_inputs.project_term_units

    @root_validator(skip_on_failure=True)
    def check_dam_award_against_config(cls, values):
        _check_dam_award_against_config(values)
        return values

    @root_validator(skip_on_failure=True)
    def check_time_intervals(cls, values):
        assert (
            values["time_interval_mins"] <= values["pv_inputs"].time_interval_mins
        ), "price time_interval_mins must less than or equal to pv time_interval_mins"
        return values

    @root_validator(skip_on_failure=True)
    def check_price_time_interval_against_pv_project_term(cls, values):
        price_str, price = _get_price_str_and_price(values)
        _check_time_interval_project_term(
            len(price),
            price_str,
            values["pv_inputs"].project_term,
            values["time_interval_mins"],
            values["pv_inputs"].project_term_units,
        )
        return values

    @root_validator(skip_on_failure=True)
    def check_battery_terms(cls, values):
        if len(values["storage_inputs"].batteries) > 1:
            total_batt_yrs = sum(bat.term for bat in values["storage_inputs"].batteries)
            assert (
                scale_project_term_to_hours(values["pv_inputs"].project_term, values["pv_inputs"].project_term_units)
                >= total_batt_yrs * 8760
            ), "project_term must be greater than or equal to the total battery terms"
        return values

    @root_validator(skip_on_failure=True)
    def check_degrad_table_length(cls, values):
        return _check_degrad_table_length(values)

    @root_validator(skip_on_failure=True)
    def check_sym_reg_inputs(cls, values):
        return _check_symmetric_reg_inputs(values)

    @validator("storage_inputs")
    def set_default_solver(cls, v: MultiStorageInputs):
        if v.solver_config.solver is None:
            v.solver_config.solver = Solver.GLPK_HiGHS
        return v


class StandaloneStorageModel(ProjectTermMixin, ImportExportLimitMixin, MarketBase):
    """Simulation class for standalone storage simulations"""

    project_type: t.Optional[t.Literal["storage"]] = "storage"
    """Used by the API for model-type discrimination, can be ignored"""
    storage_inputs: MultiStorageInputs
    """Submodel for BESS design, market participation and optimization"""
    downstream_system: t.Optional[DownstreamSystem]
    """Optional submodel for detailed treatment of losses. The point at which detailed losses are considered can be
    controlled with :attr:`DownstreamSystem.model_losses_from`
    """
    ambient_temp: t.Optional[t.List[float]]
    """Optional time series of ambient temperature data to be used with :attr:`BatteryParams.hvac`
    
    - Units: |degrees|\ C
    """

    @root_validator(skip_on_failure=True)
    def check_dam_award_against_config(cls, values):
        _check_dam_award_against_config(values)
        return values

    @root_validator(skip_on_failure=True)
    def check_ambient_temp_length(cls, values):
        if values["ambient_temp"]:
            price_str, price = _get_price_str_and_price(values)
            _check_lengths({price_str: price, "ambient_temp": values["ambient_temp"]})
        return values

    @root_validator(skip_on_failure=True)
    def check_time_interval_project_term(cls, values):
        price_str, price = _get_price_str_and_price(values)
        _check_time_interval_project_term(
            len(price), price_str, values["project_term"], values["time_interval_mins"], values["project_term_units"]
        )
        return values

    @root_validator(skip_on_failure=True)
    def check_battery_and_project_terms(cls, values):
        # only validate battery terms if a battery term is passed or multiple batteries are passed
        if len(values["storage_inputs"].batteries) > 1 or values["storage_inputs"].batteries[0].term is not None:
            total_batt_yrs = sum(bat.term for bat in values["storage_inputs"].batteries)
            project_term_hours = scale_project_term_to_hours(values["project_term"], values["project_term_units"])
            total_battery_term_hours = int(total_batt_yrs * 8760)
            assert (
                project_term_hours == total_battery_term_hours
            ), "project_term must be consistent with the total battery terms"
            price_str, price = _get_price_str_and_price(values)
            price_hours = int(len(price) * (values["time_interval_mins"] / 60))
            assert (
                price_hours >= total_battery_term_hours
            ), f"length of {price_str} must be greater than total battery terms"
        return values

    @root_validator(skip_on_failure=True)
    def check_degrad_table_length(cls, values):
        return _check_degrad_table_length(values)

    @root_validator(skip_on_failure=True)
    def check_sym_reg_inputs(cls, values):
        return _check_symmetric_reg_inputs(values)

    @validator("storage_inputs")
    def set_default_solver(cls, v: MultiStorageInputs):
        if v.solver_config.solver is None:
            v.solver_config.solver = Solver.HiGHS_GLPK
        return v


def get_pv_model(**data: t.Any) -> GenerationModel:
    """:meta private:"""
    try:
        m = PVGenerationModel(**data)
    except ValidationError:
        try:
            m = DCExternalGenerationModel(**data)
        except ValidationError:
            m = ACExternalGenerationModel(**data)
    return m


def get_pv_storage_model(**data: t.Any) -> PVStorageModel:
    """:meta private:"""
    return PVStorageModel(**data)


def get_standalone_storage_model(model: dict) -> StandaloneStorageModel:
    """:meta private:"""
    return StandaloneStorageModel(**model)


JobModel = Annotated[
    t.Union[StandaloneStorageModel, PVStorageModel, GenerationModel], Field(discriminator="project_type")
]


@optional_discriminators(["model"])
class AsyncModelBase(BaseModel):
    """:meta private:"""

    id: str
    model: JobModel
    results_path: t.Optional[str]


@optional_discriminators(["model"])
class AsyncPVModel(AsyncModelBase):
    """:meta private:"""

    id: str
    model: GenerationModel


class AsyncPVStorageModel(AsyncModelBase):
    """:meta private:"""

    id: str
    model: PVStorageModel


class AsyncStandaloneStorageModel(AsyncModelBase):
    """:meta private:"""

    id: str
    model: StandaloneStorageModel
