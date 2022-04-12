from raw_data_hourly import RAW_DATA_HOURLY_2018, RAW_DATA_HOURLY_2018_HEADERS

solarKwToKwhYearly = 1700  # solar average yearly production hours [hrs/yr]
windKwToKwhYearly = 3014  # wind average yearly production hours [hrs/yr]
predicted_year = 2030
predicted_solar_capacity = 30000  # [MW]
predicted_wind_capacity = 500  # [MW]
predicted_storage_energy_capacity = 50000  # [MWh]

usd_exchange_rate = 3.5  # [ILS/USD]
eur_exchange_rate = 4.0  # [ILS/EUR]
wacc = 0.05  # [weighted average cost of capital]
interest_rate = 0.03

ccgt_co2 = 397  # [g/kwh]
ccgt_sox = 0  # [g/kwh]
ccgt_nox = 0.16  # [g/kwh]
ccgt_pmx = 0.02  # [g/kwh]


def sum_data(header):
    header_index = RAW_DATA_HOURLY_2018_HEADERS.index(header)
    return sum([line[header_index] for line in RAW_DATA_HOURLY_2018])


solar_capacity_2018 = sum_data("SOLAR") / solarKwToKwhYearly
wind_capacity_2018 = sum_data("WIND") / windKwToKwhYearly
total_demand_2018 = sum_data("TOTAL PRODUCTION")
