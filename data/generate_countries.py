from typing import List

import pandas as pd
from jinja2 import Template


class GeneratedCountry:
    def __init__(self, country: str):
        self.country = country

    @property
    def variable_name(self):
        name = self.country.replace(' ', '_')
        name = name.replace('(', '').replace(')', '')
        name = name.replace(',', '_').replace(':', "")
        name = name.replace('-', '').replace('/', '_')
        name = name.replace(' ', '_').replace('.', '')
        name = name.replace("'", '')
        return name

    def __repr__(self):
        return f"<country: {self.country} />"


def load_countries() -> List[GeneratedCountry]:
    """
    Load list of available countries from UN's dataset
    :return:
    """
    data = pd.read_csv('../WPP2019_TotalPopulationBySex.csv')
    countries = data['Location'].drop_duplicates().tolist()
    l = [GeneratedCountry(c) for c in countries]
    return l


if __name__ == '__main__':
    with open('countries.j2', 'r') as f:
        template = Template(f.read())

    countries = load_countries()
    generated = template.render(countries=load_countries())
    with open('countries.py', 'w') as f:
        f.write(generated)
