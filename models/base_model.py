from typing import Dict, List
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
from random import randint


class BaseValue:
    def __init__(self, label, value) -> None:
        self.label = label
        self.value = value


class BaseModel:
    def __init__(self, title="Model", xLabel="Days", yLabel="Number of people", labels=['S', 'E', 'I', 'R']):
        self.title = title
        self.xLabel = xLabel
        self.yLabel = yLabel
        self.values_dict: Dict[str, List[BaseValue]] = {}
        self.labels: List[str] = labels
        self.days: List[int] = []
        self.index = count()

    def compute(self, days=1):
        raise NotImplementedError

    def values(self) -> List[BaseValue]:
        raise NotImplementedError

    def __plot__(self):

        for label in self.labels:
            vs = self.values_dict[label]
            vs_list = [v.value for v in vs]
            plt.plot(self.days, vs_list,  label=label)

        plt.xlabel(self.xLabel)
        plt.ylabel(self.yLabel)
        plt.title(self.title)
        plt.legend()

    def __simulate_one_day__(self):
        self.compute()
        self.days.append(next(self.index))

    def __add_one_day_values__(self):
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

    def draw_graph_at(self, days=50) -> plt:
        for i in range(days):
            self.__simulate_one_day__()
            self.__add_one_day_values__()
        self.__plot__()
        plt.savefig(f"{self.title}-{days}.png")
        plt.show()

    def animate_graph(self, figure_number=1):
        fig = plt.figure(figure_number)
        ani = FuncAnimation(fig, self.__animate__, interval=1000)
        fig.tight_layout()
        plt.show()
