from configparser import ConfigParser
from pathlib import Path
from typing import Dict, List
from .constants import BashColors as bc
from .assets import trim_path_string


class Configure:
    def __init__(
        self,
        config_settings: Dict,
        path_config_file: str | Path,
        numeric_vars: List[str] = None,
        mandatory_vars: List[str] = None
    ) -> None:
        """
        Structure of the config file:
        [header]
        param1 = \n
        param2 = \n
        @config_settings: 
        Dictionary of which the keys are the headers and associated values are the parameters: List | Tuple

        @path_config_file:
        Pathname of the config file

        @numeric_vars
        List of the variables that are supposed to be numeric

        @mandatory_vars
        Variables whose existence in the config file are mandatory. Default all variables are mandatory
        """
        self.config_settings = config_settings
        self.path_config_file = path_config_file
        self.numeric_vars = numeric_vars
        self.mandatory_vars = mandatory_vars

    def prepare_input_params(self) -> Dict:
        try:
            parameters = {}
            config = ConfigParser()
            config.read(self.path_config_file)

            for header, variables_names in self.config_settings.items():
                for variable_name in variables_names:
                    variable = config.get(header, variable_name)
                    if self.mandatory_vars is None:
                        if not variable:
                            raise Exception(
                                f"{bc.BRed}Please provide information for {variable_name}{bc.Reset}\n")

                    else:
                        if variable_name in self.mandatory_vars and not variable:
                            raise Exception(
                                f"{bc.BRed}Please provide information for {variable_name}{bc.Reset}\n")

                    variable = trim_path_string(variable)
                    parameters[variable_name] = variable

            return parameters

        except Exception as e:
            raise Exception(
                f"{bc.BRed}Failed to extract input parameters{bc.Reset}\n", e)

    def handle_numerics(self, parameters: Dict):
        for key, value in parameters.items():
            if key in self.numeric_vars:
                try:
                    parameters[key] = float(value)

                except ValueError as ve:
                    raise ValueError(
                        f"{bc.BRed}Failed to convert {key} to float{bc.Reset}\n", ve)
        return parameters
