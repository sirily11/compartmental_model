from models.seir_model import SEIRModel
from models.sir_model import SIRModel
from data.country_data import CountryData
from data.countries import Countries

# Load data from database
country_data = CountryData().load(Countries.United_States_of_America)

# Use model
total_days = 10
# model = SEIRModel(population=country_data.population,
#                   per_capita_natural_death_rate=country_data.deaths_per_thousand / 1000,
#                   per_capita_birth_rate=country_data.births_per_thousand / 1000)
# model.animate_graph()

model = SIRModel(population=country_data.population,
                  per_capita_natural_death_rate=country_data.deaths_per_thousand / 1000,
                  per_capita_birth_rate=country_data.births_per_thousand / 1000, i_init=100)
model.draw_graph_at(100)