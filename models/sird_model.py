from typing import List

from data.countries import Countries
from .base_model import BaseModel, BaseValue


class SIRDModel(BaseModel):
    s = 0
    r = 0
    i = 0
    d = 0

    def __init__(self, population=1000000, virus_induced_acerage_fatlity_rate=0.006, per_capita_natural_death_rate=0,
                 per_capita_birth_rate=0,
                 probability_of_disease_transmission=0.75, rate_of_progression_from_exposed=1 / 3, recovery_rate=1 / 8,
                 r_init=0, i_init=0, d_init=0, country: Countries = None):
        super().__init__(labels=['Susceptible', 'Infectious', 'Recovered', 'Deceased'], title='SIRD Model',
                         per_capita_natural_death_rate=per_capita_natural_death_rate,
                         per_capita_birth_rate=per_capita_birth_rate,
                         probability_of_disease_transmission=probability_of_disease_transmission,
                         rate_of_progression_from_exposed=rate_of_progression_from_exposed,
                         virus_induced_acerage_fatlity_rate=virus_induced_acerage_fatlity_rate, population=population,
                         recovery_rate=recovery_rate, country=country)

        self.s = population - r_init - i_init - d_init
        self.r = r_init
        self.i = i_init
        self.d = d_init
        self.current_day = 0

    @property
    def n(self):
        return max(self.s + self.i + self.r - self.d, 1)

    @property
    def s_dot(self):
        return - self.probability_of_disease_transmission * self.i * self.s / self.n

    @property
    def d_dot(self):
        return self.per_capita_natural_death_rate * self.i

    @property
    def r_dot(self):
        return self.recovery_rate * self.i

    @property
    def i_dot(self):
        return min(self.probability_of_disease_transmission * self.i * self.s / self.n * \
               self.recovery_rate * self.i * self.per_capita_natural_death_rate * self.i, self.init_population)

    def compute(self, day: float = 1):
        s = day * self.s_dot
        r = day * self.r_dot
        i = day * self.i_dot
        d = day * self.d_dot

        self.s += s
        self.r += r
        self.i += i
        self.d += d

        self.current_day += day

    def values(self) -> List[BaseValue]:
        return [
            BaseValue('Susceptible', self.s),
            BaseValue('Infectious', self.i),
            BaseValue('Recovered', self.r),
            BaseValue('Deceased', self.d)
        ]
