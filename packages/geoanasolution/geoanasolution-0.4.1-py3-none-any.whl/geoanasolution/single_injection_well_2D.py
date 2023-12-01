import math
import numpy as np
from ._analytical_base import AnalyticalSolutionBase


class SingleInjectionWell2D(AnalyticalSolutionBase):
    def __init__(self):
        super().__init__()

        # necessary parameters
        self.AQUIFER_CONDUCTIVITY = "AQUIFER_CONDUCTIVITY"
        self.AQUIFER_DENSITY = "AQUIFER_DENSITY"
        self.AQUIFER_SPECIFIC_HEAT_CAPACITY = "AQUIFER_SPECIFIC_HEAT_CAPACITY"
        self.FLOW_RATE = "FLOW_RATE"
        self.FLUID_DENSITY = "FLUID_DENSITY"
        self.FLUID_SPECIFIC_HEAT_CAPACITY = "FLUID_SPECIFIC_HEAT_CAPACITY"
        self.INITIAL_TEMPERATURE = "INITIAL_TEMPERATURE"
        self.INJECTION_TEMPERATURE = "INJECTION_TEMPERATURE"
        self.THICK = "THICK"
        self.TIME = "TIME"

        # initialize necessary parameters
        self._add_param(self.AQUIFER_CONDUCTIVITY, 0)
        self._add_param_info(self.AQUIFER_CONDUCTIVITY, "W/(m∙k)", "0", "The aquifer means the fluid-solid mixture.")
        self._add_param(self.AQUIFER_DENSITY, 0)
        self._add_param_info(self.AQUIFER_DENSITY, "kg/m^3", "0")
        self._add_param(self.AQUIFER_SPECIFIC_HEAT_CAPACITY, 0)
        self._add_param_info(self.AQUIFER_SPECIFIC_HEAT_CAPACITY, "J/(Kg∙K)", "0")
        self._add_param(self.FLOW_RATE, 0)
        self._add_param_info(self.FLOW_RATE, "kg/s", "0", "It is positive for injection and vice versa.")
        self._add_param(self.FLUID_DENSITY, 1000)
        self._add_param_info(self.FLUID_DENSITY, "kg/m^3", "1000")
        self._add_param(self.FLUID_SPECIFIC_HEAT_CAPACITY, 4185)
        self._add_param_info(self.FLUID_SPECIFIC_HEAT_CAPACITY, "J/(Kg∙K)", "4185")
        self._add_param(self.INITIAL_TEMPERATURE, 0)
        self._add_param_info(self.INITIAL_TEMPERATURE, "°C", "0")
        self._add_param(self.INJECTION_TEMPERATURE, 0)
        self._add_param_info(self.INITIAL_TEMPERATURE, "°C", "0")
        self._add_param(self.THICK, 1)
        self._add_param_info(self.THICK, "m", "1", "The aquifer thick.")
        self._add_param(self.TIME, 0)
        self._add_param_info(self.TIME, "s", "0")

    def calc(self, coordinate):
        if not isinstance(coordinate, np.ndarray):
            raise TypeError("The input coordinate must in the type of np.ndarray")

        # The volumetric flow rate.
        q = self.__q/self.__rho_f
        # The middle parameters.
        nu = q*self.__rho_f*self.__cp_f/(4*math.pi*self.__b*self.__lambda)
        tau = 4*self.__lambda*self.__t/(self.__rho*self.__cp*self.__b*self.__b)

        # The calculation process.
        r = np.linalg.norm(coordinate)
        omega = 2*r/self.__b
        result = math.gamma(nu) - self.__gamma_inc(nu, omega**2/(4*tau))
        result /= math.gamma(nu)
        result *= self.__t_in - self.__t_ini
        result += self.__t_ini

        return result

    def doc(self):
        print("[GeoAnaSolution] Parameters for the model of single injection well in the 2D aquifer.")
        self._print_param_info()

    def __gamma_inc(self, s, x):
        iterations = 120
        sum = 0
        for i in range(iterations):
            sum += math.pow(x, i) / math.gamma(s + i + 1)

        return math.pow(x, s) * math.gamma(s) * math.exp(-x) * sum

    @property
    def __b(self):
        return self.get_param(self.THICK)

    @property
    def __cp(self):
        return self.get_param(self.AQUIFER_SPECIFIC_HEAT_CAPACITY)

    @property
    def __cp_f(self):
        return self.get_param(self.FLUID_SPECIFIC_HEAT_CAPACITY)

    @property
    def __lambda(self):
        return self.get_param(self.AQUIFER_CONDUCTIVITY)

    @property
    def __q(self):
        return self.get_param(self.FLOW_RATE)

    @property
    def __rho(self):
        return self.get_param(self.AQUIFER_DENSITY)

    @property
    def __rho_f(self):
        return self.get_param(self.FLUID_DENSITY)

    @property
    def __t(self):
        return self.get_param(self.TIME)

    @property
    def __t_in(self):
        return self.get_param(self.INJECTION_TEMPERATURE)

    @property
    def __t_ini(self):
        return self.get_param(self.INITIAL_TEMPERATURE)
