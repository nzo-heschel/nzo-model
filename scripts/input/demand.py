# Demand
# https://www.boi.org.il/he/Research/DocLib/dp201713h.pdf
demand_baseline_value = 72.5  # [TWh] 2019 value
efficiency_targets_pct = {2020: 0, 2030: 7, 2040: 15, 2050: 25}  # [%]
yearly_growth_pct = {2020: 2.8, 2030: 2.8, 2040: 2.8, 2050: 2.8}  # [%]

# Industry
industry_conversion_factor = 0.89
industry_conversion_fossil_to_electricity_pct = {2020: 0, 2030: 10, 2040: 40, 2050: 80}
industry_efficiency_reduction_pct = {2020: 0, 2030: 5, 2040: 15, 2050: 25}
industry_fuel_baseline_twh = 22.6  #

# Transportation
# https://www.cbs.gov.il/he/mediarelease/pages/2020/נסועה-בשנת-2019.aspx
# https://ev-database.org/cheatsheet/energy-consumption-electric-car
# https://about.bnef.com/electric-vehicle-outlook/
# https://www.gov.il/he/Departments/policies/2015_dec542
transportation_baseline_bkm = 63.2
transportation_growth_yearly_pct = {2020: 2.8, 2030: 2.8, 2050: 2.8}
transportation_shift_to_public_pct = {2020: 0, 2030: 0, 2040: 15, 2050: 25}
transportation_conversion_to_ev_pct = {2020: 0, 2030: 25, 2040: 50, 2050: 100}
transportation_ev_efficiency_improvement_pct = {2020: 0, 2030: 0, 2050: 0}
transportation_kwh_per_km = 0.2
