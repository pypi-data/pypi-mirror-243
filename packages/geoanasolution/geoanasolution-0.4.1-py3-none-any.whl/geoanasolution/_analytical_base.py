class AnalyticalSolutionBase:
    def __init__(self):
        self.__param = {}
        self.__param_info = []

    def _add_param(self, param_name, value):
        if param_name in self.__param:
            raise RuntimeError("The input parameter name has existed in the map.")
        else:
            self.__param[param_name] = value

    def _add_param_info(self, name, unit, default, introduction=""):
        self.__param_info.append({"NAME": name, "UNIT":unit, "DEFAULT":default, "INTRODUCTION":introduction})

    def _print_param_info(self):
        max_name = max(max(len(item["NAME"]) for item in self.__param_info), 4) + 2
        max_unit = max(max(len(item["UNIT"]) for item in self.__param_info), 4) + 2
        max_default = max(max(len(item["DEFAULT"]) for item in self.__param_info), 7) + 2
        max_introduction = max(max(len(item["INTRODUCTION"]) for item in self.__param_info), 12) + 2
        prefix = " * "

        # Print a separator
        print(prefix+"-"*max_name+"|"+"-"*max_unit+"|"+"-"*max_default+"|"+"-"*max_introduction)

        # Print the header
        name_head = " NAME".ljust(max_name)
        unit_head = " UNIT".ljust(max_unit)
        default_head = " DEFAULT".ljust(max_default)
        introduction_head = " INTRODUCTION".ljust(max_introduction)
        print(prefix+f"{name_head}|{unit_head}|{default_head}|{introduction_head}")

        # Print a separator
        print(prefix+"-"*max_name+"|"+"-"*max_unit+"|"+"-"*max_default+"|"+"-"*max_introduction)

        # Print the parameters information
        for item in self.__param_info:
            name = (" "+item["NAME"]).ljust(max_name)
            unit = (" "+item["UNIT"]).ljust(max_unit)
            default = (" "+item["DEFAULT"]).ljust(max_default)
            introduction = (" "+item["INTRODUCTION"]).ljust(max_introduction)

            print(prefix+f"{name}|{unit}|{default}|{introduction}")

        # Print a separator
        print(prefix+"-"*max_name+"|"+"-"*max_unit+"|"+"-"*max_default+"|"+"-"*max_introduction)

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


