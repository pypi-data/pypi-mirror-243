import math
import numpy as np
from ._analytical_base import AnalyticalSolutionBase


class Theis(AnalyticalSolutionBase):
    def __init__(self):
        super().__init__()

        # necessary parameters
        self.FLOW_RATE = "FLOW_RATE"
        self.G = "G"
        self.INITIAL_VALUE = "INITIAL_VALUE"
        self.PERMEABILITY = "PERMEABILITY"
        self.STORAGE = "STORAGE"
        self.THICK = "THICK"
        self.TIME = "TIME"
        self.WATER_DENSITY = "WATER_DENSITY"
        self.WATER_VISCOSITY = "WATER_VISCOSITY"
        self.WELL_COORDINATE = "WELL_COORDINATE"

        # initialize necessary parameters
        self._add_param(self.FLOW_RATE, 0)
        self._add_param_info(self.FLOW_RATE, "m^3/s", "0", "The injection well is positive and vice versa.")
        self._add_param(self.G, 9.8)
        self._add_param_info(self.G, "m/(s^2)", "9.8", "The gravity acceleration.")
        self._add_param(self.INITIAL_VALUE, 0)
        self._add_param_info(self.INITIAL_VALUE, "m", "0", "The initial head of the field.")
        self._add_param(self.PERMEABILITY, 0)
        self._add_param_info(self.PERMEABILITY, "m^2", "0")
        self._add_param(self.STORAGE, 0)
        self._add_param_info(self.STORAGE, "m^(-1)", "0")
        self._add_param(self.THICK, 1)
        self._add_param_info(self.THICK, "m", "1", "The aquifer thick.")
        self._add_param(self.TIME, 0)
        self._add_param_info(self.TIME, "s", "0", "The production time.")
        self._add_param(self.WATER_DENSITY, 1000)
        self._add_param_info(self.WATER_DENSITY, "kg/m^3", "1000")
        self._add_param(self.WATER_VISCOSITY, 1.01e-3)
        self._add_param_info(self.WATER_VISCOSITY, "Pa∙s", "1.01e-3")
        self._add_param(self.WELL_COORDINATE, np.array([0.0, 0.0, 0.0]))
        self._add_param_info(self.WELL_COORDINATE, "m", "(0, 0, 0)", "This is a np.ndarray.")

        # calculation using parameters
        self.__a = [-0.57721566, 0.99999193, -0.24991055, 0.05519968, -0.00976004, 0.00107857]
        self.__b = [0.2677737343, 8.6347608925, 18.059016973, 8.5733287401]
        self.__c = [3.9584969228, 21.0996530827, 25.6329561486, 9.5733223454]

    def calc(self, coordinate):
        if not isinstance(coordinate, np.ndarray):
            raise TypeError("The input coordinate must in the type of np.ndarray")

        well_coordinate = self.get_param(self.WELL_COORDINATE)
        permeability_coe = self.get_param(self.PERMEABILITY)*self.get_param(self.WATER_DENSITY)*self.get_param(self.G)
        permeability_coe = self.get_param(self.THICK)*permeability_coe/self.get_param(self.WATER_VISCOSITY)
        radius = np.linalg.norm(coordinate - well_coordinate)
        u = self.get_param(self.STORAGE)*self.get_param(self.THICK)/(4*permeability_coe*self.get_param(self.TIME))
        u = u*radius**2

        head_change = self.get_param(self.FLOW_RATE)*self.__calc_series_num(u)/(4*math.pi*permeability_coe)

        return self.get_param(self.INITIAL_VALUE) + head_change

    def doc(self):
        print("[GeoAnaSolution] Parameters for the Theis model.")
        self._print_param_info()

    def __calc_series_num(self, u):
        if u < 1:
            tmp = self.__a[0] + u*(self.__a[1] + u*(self.__a[2] + u*(self.__a[3] + u*(self.__a[4] + u*self.__a[5]))))
            return -1*math.log(u) + tmp
        else:
            tmp1 = 1/(u*(math.e**u))
            tmp2 = self.__b[0] + u*(self.__b[1] + u*(self.__b[2] + u*(self.__b[3] + u)))
            tmp3 = self.__c[0] + u*(self.__c[1] + u*(self.__c[2] + u*(self.__c[3] + u)))
            return tmp1*tmp2/tmp3
