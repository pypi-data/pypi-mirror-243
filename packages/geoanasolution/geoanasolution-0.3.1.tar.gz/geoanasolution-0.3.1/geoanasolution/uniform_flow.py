import math
import numpy as np
from ._analytical_base import AnalyticalSolutionBase


class UniformFlow(AnalyticalSolutionBase):
    def __init__(self):
        super().__init__()

        # necessary parameters
        self.DIFFUSION_COE = "DiffusionCoe"
        self.INITIAL_VALUE = "InitialValue"
        self.VELOCITY = "Velocity"

        # initialize necessary parameters
        self._add_param(self.DIFFUSION_COE, 0)
        self._add_param(self.INITIAL_VALUE, 0)
        self._add_param(self.VELOCITY, 0)

    def calc(self, sample_coordinate):
        if not isinstance(sample_coordinate, np.ndarray):
            raise TypeError("The input coordinate must in the type of np.ndarray")

        coe = math.sqrt((4*self.get_param(self.DIFFUSION_COE)*sample_coordinate[0])/self.get_param(self.VELOCITY))
        upgrade_value = self.get_param(self.INITIAL_VALUE)*math.erfc(sample_coordinate[1]/coe)

        return upgrade_value