import pandas as pd
from data.countries import Countries


class CountryData:
    births_per_thousand = 0
    deaths_per_thousand = 0
    population = 0
    year = 0
    country: Countries = None

    def __init__(self):
        self.population_data = pd.read_csv('WPP2019_TotalPopulationBySex.csv')
        self.birth_date = pd.read_csv('WPP2019_Fertility_by_Age.csv')

    def load(self, country: Countries, year=2019):
        self.country = country
        selected_country = self.population_data[(self.population_data['Location'] == str(country.value))
                                                & (self.population_data['Time'] == year)]
        selected_country_birth_death = self.birth_date[self.birth_date['Location'] == str(country.value)]
        selected_country_birth_death = selected_country_birth_death[
            selected_country_birth_death['Date'].str.contains(str(year))]
        for value in selected_country[['PopTotal']].tail().values:
            self.population = value[0] * 1000

        for value in selected_country_birth_death[['CBR', 'CDR']].tail().values:
            self.births_per_thousand = value[0]
            self.deaths_per_thousand = value[1]
        return self

