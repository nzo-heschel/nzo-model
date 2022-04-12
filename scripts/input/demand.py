demand_baseline_year = 2019
first_year = 2020
last_year = 2050
demand_baseline_value = 72.5  # [TWh]
efficiency_targets_pct = {2020: 0, 2030: 7, 2040: 15, 2050: 25}  # [%]
# based on https://www.boi.org.il/he/Research/DocLib/dp201713h.pdf
yearly_growth_pct: dict[int, float] = {2020: 2.8, 2030: 2.8, 2040: 2.8, 2050: 2.8}  # [%]

# Industry
industry_conversion_factor = 0.89
industry_conversion_fossil_to_electricity_pct = {2020: 0, 2030: 10, 2040: 40, 2050: 80}
industry_efficiency_reduction_pct = {2030: 5, 2040: 15, 2050: 25}
industry_fuel_baseline_twh = 22.6  #


# =============================================== #

