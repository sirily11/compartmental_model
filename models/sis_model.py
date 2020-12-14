from data.countries import Countries
from .base_model import BaseModel, BaseValue


class SISModel(BaseModel):
    s = 0
    i = 0
    r = 0

    def __init__(self, population=1000000, virus_induced_acerage_fatlity_rate=0.006, per_capita_natural_death_rate=0,
                 per_capita_birth_rate=0,
                 probability_of_disease_transmission=0.75, rate_of_progression_from_exposed=1 / 3, recovery_rate=1 / 8,
                 i_init=0, country: Countries = None):
        super().__init__(labels=['Susceptible', 'Infectious'], title='SIS Model',
                         per_capita_natural_death_rate=per_capita_natural_death_rate,
                         per_capita_birth_rate=per_capita_birth_rate,
                         probability_of_disease_transmission=probability_of_disease_transmission,
                         rate_of_progression_from_exposed=rate_of_progression_from_exposed,
                         virus_induced_acerage_fatlity_rate=virus_induced_acerage_fatlity_rate, population=population,
                         recovery_rate=recovery_rate, country=country)

        self.s = population - i_init
        self.i = i_init
        self.current_day: float = 0

    @property
    def n(self):
        return self.s + self.i

    @property
    def s_dot(self):
        return - self.probability_of_disease_transmission * self.s * self.i / self.n + self.recovery_rate * self.i

    @property
    def i_dot(self):
        return self.probability_of_disease_transmission * self.s * self.i / self.n - self.recovery_rate * self.i

    def compute(self, day: float = 1):
        """
        Compute the final result 1 day after
        """
        s = day * self.s_dot
        i = day * self.i_dot

        self.s += s
        self.i += i
        self.current_day += day

    def values(self):
        return [
            BaseValue('Susceptible', self.s),
            BaseValue('Infectious', self.i),
        ]
