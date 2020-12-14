from typing import Dict, List
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
from random import randint
from os.path import join, exists
from os import makedirs

from data.countries import Countries


class BaseValue:
    def __init__(self, label, value) -> None:
        self.label = label
        self.value = value


class BaseModel:
    # Λ
    per_capita_birth_rate = 0
    # μ
    per_capita_natural_death_rate = 0
    # α
    virus_induced_average_fatality_rate = 0
    # β
    probability_of_disease_transmission = 0
    # ϵ
    rate_of_progression_from_exposed = 0
    # γ
    recovery_rate = 0
    # N0
    init_population = 0

    def __init__(self, title="Model", xLabel="Days", yLabel="Number of people", labels=['S', 'E', 'I', 'R'],
                 population=1000000, virus_induced_acerage_fatlity_rate=0.006, per_capita_natural_death_rate=0,
                 per_capita_birth_rate=0,
                 probability_of_disease_transmission=0.75, rate_of_progression_from_exposed=1 / 3,
                 recovery_rate=1 / 8, country: Countries = None):
        """
        Construct a model
        :param title: Model's title
        :param xLabel: Plot x axis's label
        :param yLabel: Plot y axis's label
        :param labels: List of labels you will have for your plot
        :param population: Init population
        :param virus_induced_acerage_fatlity_rate:
        :param per_capita_natural_death_rate:
        :param per_capita_birth_rate:
        :param probability_of_disease_transmission:
        :param rate_of_progression_from_exposed:
        :param recovery_rate:
        :param country: Which country
        """
        self.title = title
        self.xLabel = xLabel
        self.yLabel = yLabel
        self.values_dict: Dict[str, List[BaseValue]] = {}
        self.labels: List[str] = labels
        self.days: List[int] = []
        self.index = count()

        self.init_population = population
        self.per_capita_birth_rate = per_capita_birth_rate
        self.per_capita_natural_death_rate = per_capita_natural_death_rate
        self.virus_induced_average_fatality_rate = virus_induced_acerage_fatlity_rate
        self.probability_of_disease_transmission = probability_of_disease_transmission
        self.rate_of_progression_from_exposed = rate_of_progression_from_exposed
        self.recovery_rate = recovery_rate
        self.country = country

    def compute(self, days=1):
        """
        Compute the result for the future.
        :pa
        """
        raise NotImplementedError

    def values(self) -> List[BaseValue]:
        """
        Return a list of simulation values.
        :return:
        """
        raise NotImplementedError

    def __plot__(self):
        """
        Plot data
        :return:
        """
        for label in self.labels:
            vs = self.values_dict[label]
            vs_list = [v.value for v in vs]
            plt.plot(self.days, vs_list, label=label)

        plt.xlabel(self.xLabel)
        plt.ylabel(self.yLabel)
        plt.title(self.title)
        plt.legend()

    def __simulate_one_day__(self):
        """
        Make one day prediction
        :return:
        """
        self.compute()
        self.days.append(next(self.index))

    def __add_one_day_values__(self):
        """
        Input one day's value into the list
        :return:
        """
        values = self.values()
        for value in values:
            ls = []
            if value.label in self.values_dict:
                ls = self.values_dict[value.label]
                ls.append(value)
            else:
                ls = [value]
            self.values_dict[value.label] = ls

    def __animate__(self, i):
        self.__simulate_one_day__()
        self.__add_one_day_values__()
        plt.cla()
        self.__plot__()

    def draw_graph_at(self, days=50, path="./results") -> str:
        """
        Draw data.
        :param path: save path
        :param days: Number day step
        :return:
        """
        for i in range(days):
            self.__simulate_one_day__()
            self.__add_one_day_values__()
        self.__plot__()
        file_name = f"{self.title}-{days}.png"
        folder_name = join(path, 'graphs', str(self.country.value))
        file_name = join(folder_name, file_name)
        output_file_name = join('graphs', str(self.country.value), f"{self.title}-{days}.png")
        if not exists(folder_name):
            makedirs(folder_name)

        plt.savefig(file_name)
        plt.clf()
        return output_file_name

    def animate_graph(self, figure_number=1):
        """
        Animate data
        :param figure_number:
        :return:
        """
        fig = plt.figure(figure_number)
        ani = FuncAnimation(fig, self.__animate__, interval=1000)
        fig.tight_layout()
        plt.show()
