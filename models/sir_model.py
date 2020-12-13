from .base_model import BaseModel, BaseValue


class SIRModel(BaseModel):
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
    s = 0
    e = 0
    i = 0
    r = 0
    # N0
    init_population = 0

    def __init__(self, population=1000000, virus_induced_acerage_fatlity_rate=0.006, per_capita_natural_death_rate=0,
                 per_capita_birth_rate=0,
                 probability_of_disease_transmission=0.75, rate_of_progression_from_exposed=1/3, recovery_rate=1/8, e_init=20000, i_init=0, r_init=0):

        super().__init__(labels=['Susceptible', 'Infectious', 'Recovered'], title='SIR Model')
        self.init_population = population
        self.s = population - e_init - i_init
        self.per_capita_birth_rate = per_capita_birth_rate
        self.per_capita_natural_death_rate = per_capita_natural_death_rate
        self.virus_induced_average_fatality_rate = virus_induced_acerage_fatlity_rate
        self.probability_of_disease_transmission = probability_of_disease_transmission
        self.rate_of_progression_from_exposed = rate_of_progression_from_exposed
        self.recovery_rate = recovery_rate
        self.e = e_init
        self.i = i_init
        self.r = r_init
        self.current_day: float = 0

    @property
    def n(self):
        return self.s + self.i + self.r + self.e

    @property
    def s_dot(self):
        """
        https://www.frontiersin.org/articles/10.3389/fpubh.2020.00230/full
        """
        return - self.probability_of_disease_transmission * self.s * self.i / self.n

    @property
    def i_dot(self):
        return self.probability_of_disease_transmission * self.s * self.i / self.n - self.recovery_rate * self.i

    @property
    def r_dot(self):
        return self.recovery_rate * self.i

    def compute(self, day: float = 1):
        """
        Compute the final result 1 day after
        """
        s = day * self.s_dot
        i = day * self.i_dot
        r = day * self.r_dot

        self.s += s
        self.i += i
        self.r += r
        self.current_day += day

    def values(self):
        return [
            BaseValue('Susceptible', self.s),
            BaseValue('Infectious', self.i),
            BaseValue('Recovered', self.r),
        ]
