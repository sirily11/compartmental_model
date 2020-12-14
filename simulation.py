from typing import List
from jinja2 import Template
from models import SEIRModel, SIRModel, SEISModel, SIRDModel, BaseModel, SISModel, SEIRSocialDistanceModel
from data.country_data import CountryData
from data.countries import Countries
from tqdm import tqdm


class Data:
    def __init__(self, country, paths):
        self.country = country
        self.paths = paths


def generate_data_for_all_countries():
    data_list: List[Data] = []
    # Add new model here
    models = [SEIRModel, SEIRSocialDistanceModel, SIRDModel, SIRModel, SEISModel, SISModel]

    for country in tqdm(Countries):
        # Load data from database
        country_data = CountryData().load(country)
        paths = []
        for Model in models:
            model = Model(population=country_data.population,
                          per_capita_natural_death_rate=country_data.deaths_per_thousand / 1000,
                          per_capita_birth_rate=country_data.births_per_thousand / 1000, country=country, i_init=3)
            path = model.draw_graph_at(100)
            paths.append(path)

        data_list.append(Data(country=country, paths=paths))
        # if len(data_list) > 20:
        #     return data_list
    return data_list


def generate_html(data_list: List[Data]):
    countries = [d.country for d in data_list]
    with open('./results/index.j2', 'r') as f:
        template = Template(f.read())

    generated = template.render(data_list=data_list, countries=countries)
    with open('results/index.html', 'w') as f:
        f.write(generated)


generate_html(generate_data_for_all_countries())

# country = Countries.United_States_of_America
# country_data = CountryData().load(country)
# model = SIRDModel(population=country_data.population,
#                   per_capita_natural_death_rate=country_data.deaths_per_thousand / 1000,
#                   per_capita_birth_rate=country_data.births_per_thousand / 1000, country=country, i_init=3)
# model.draw_graph_at(100)
