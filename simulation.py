from models.seir_model import SEIRModel
from models.seis_model import SEISModel
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count

# US Data
# https://www.macrotrends.net/countries/USA/united-states/birth-rate#:~:text=The%20current%20birth%20rate%20for,a%200.09%25%20increase%20from%202018.
population = 331865815
birth_rate = 11.990 / 1000
death_rate = birth_rate
# end US Data

total_days = 10
# model = SEIRModel(population=population,
#                   per_capita_natural_death_rate=death_rate, per_capita_birth_rate=birth_rate)
# model.animate_graph(1)

model = SEISModel(population=population,
                  per_capita_natural_death_rate=death_rate, per_capita_birth_rate=birth_rate)
model.draw_graph_at()
