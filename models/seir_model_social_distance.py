from data.countries import Countries
from .base_model import BaseModel, BaseValue


class SEIRSocialDistanceModel(BaseModel):
    """
    A SEIR model with social distance enable based on the paper
    https://www.medrxiv.org/content/10.1101/2020.04.30.20086611v1.full.pdf
    """
    s = 0
    e = 0
    i = 0
    r = 0

    def __init__(self, population=1000000, virus_induced_acerage_fatlity_rate=0.006, per_capita_natural_death_rate=0,
                 per_capita_birth_rate=0,
                 probability_of_disease_transmission=0.75, rate_of_progression_from_exposed=1 / 3, recovery_rate=1 / 8,
                 e_init=20000, i_init=0, r_init=0, country: Countries = None):
        super().__init__(labels=['Susceptible', 'Exposed',
                                 'Infectious', 'Recovered'], title='SEIR Model With Social Distance',
                         per_capita_natural_death_rate=per_capita_natural_death_rate,
                         per_capita_birth_rate=per_capita_birth_rate,
                         probability_of_disease_transmission=probability_of_disease_transmission,
                         rate_of_progression_from_exposed=rate_of_progression_from_exposed,
                         virus_induced_acerage_fatlity_rate=virus_induced_acerage_fatlity_rate, population=population,
                         recovery_rate=recovery_rate, country=country)

        self.s = population - e_init - i_init
        self.e = e_init
        self.i = i_init
        self.r = r_init
        # lies in the
        # range 01, where 0 indicates everyone is locked down and quarantined while 1 is equivalent
        # to our base case above.
        self.social_distance = 0.5
        self.current_day: float = 0

    @property
    def n(self):
        return self.s + self.i + self.r + self.e

    @property
    def s_dot(self):
        """
        https://www.frontiersin.org/articles/10.3389/fpubh.2020.00230/full
        """
        return (self.per_capita_birth_rate - self.per_capita_natural_death_rate * self.s -
                self.probability_of_disease_transmission * self.s * self.i / self.n) * self.social_distance

    @property
    def e_dot(self):
        return self.social_distance * self.probability_of_disease_transmission * self.s * self.i / self.n - (
                self.per_capita_natural_death_rate + self.rate_of_progression_from_exposed) * self.e

    @property
    def i_dot(self):
        return self.rate_of_progression_from_exposed * self.e - (
                self.recovery_rate + self.per_capita_natural_death_rate + self.virus_induced_average_fatality_rate) * self.i

    @property
    def r_dot(self):
        return self.recovery_rate * self.i - self.per_capita_natural_death_rate * self.r

    def compute(self, day: float = 1):
        """
        Compute the final result 1 day after
        """
        s = day * self.s_dot
        e = day * self.e_dot
        i = day * self.i_dot
        r = day * self.r_dot

        self.s += s
        self.e += e
        self.i += i
        self.r += r
        self.current_day += day

    def values(self):
        return [
            BaseValue('Susceptible', self.s),
            BaseValue('Exposed', self.e),
            BaseValue('Infectious', self.i),
            BaseValue('Recovered', self.r),
        ]
