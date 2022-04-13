from scripts.input.demand import *
from util import LinearInterpolation, DemandGrowth

PCT = 0.01


class Demand:

    def __init__(self):
        # demand
        self._efficiency_reduction = LinearInterpolation(efficiency_targets_pct, PCT)
        self._growth = DemandGrowth(demand_baseline_value, yearly_growth_pct)
        # industry
        self._industry_conversion = LinearInterpolation(industry_conversion_fossil_to_electricity_pct, PCT)
        self._industry_efficiency = LinearInterpolation(industry_efficiency_reduction_pct, PCT)
        # transportation
        self._transportation_growth = DemandGrowth(transportation_baseline_bkm, transportation_growth_yearly_pct)
        self._transportation_shift_to_public = LinearInterpolation(transportation_shift_to_public_pct, PCT)
        self._transportation_conversion_to_ev = LinearInterpolation(transportation_conversion_to_ev_pct, PCT)
        self._transportation_ev_efficiency = LinearInterpolation(transportation_ev_efficiency_improvement_pct, PCT)

    def get_demand(self, year):
        _transportation = transportation_kwh_per_km * self._transportation_growth.get_value(year) \
                * (1 - self._transportation_shift_to_public.get_value(year)) \
                * self._transportation_conversion_to_ev.get_value(year) \
                * (1 - self._transportation_ev_efficiency.get_value(year))

        _industry = industry_fuel_baseline_twh * industry_conversion_factor \
                * self._industry_conversion.get_value(year) \
                * (1 - self._industry_efficiency.get_value(year))

        _demand = self._growth.get_value(year) \
                * (1 - self._efficiency_reduction.get_value(year)) \
                + _transportation \
                + _industry

        return _demand


demand = Demand()
for yr in range(2020, 2051):
    yearly_demand = demand.get_demand(yr)
    print("Total demand in", yr, "is", yearly_demand)
