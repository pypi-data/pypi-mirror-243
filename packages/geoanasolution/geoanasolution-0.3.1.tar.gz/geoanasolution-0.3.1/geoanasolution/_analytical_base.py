class AnalyticalSolutionBase:
    def __init__(self):
        self.__param = {}

    def _add_param(self, param_name, value):
        if param_name in self.__param:
            raise RuntimeError("The input parameter name has existed in the map.")
        else:
            self.__param[param_name] = value

    def get_param(self, param_name):
        if param_name in self.__param:
            return self.__param[param_name]
        else:
            raise RuntimeError("The input parameter name doesn't exist in the map.")

    def print_param(self):
        print("[GeoAnaSolution] Parameters list:")
        for key, value in self.__param.items():
            print("*", key+":", value)

    def set_param(self, param_name, value):
        if param_name in self.__param:
            self.__param[param_name] = value
        else:
            raise RuntimeError("The input parameter name doesn't exist in the map.")


