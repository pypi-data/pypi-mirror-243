from typing import List
from pathlib import Path


def trim_path_string(*args) -> List[str] | str:
    mod_args = []
    for arg in args:
        mod_args.append(arg.strip().replace("'", "").replace('"', ''))

    if len(mod_args) == 1:
        return mod_args[0]
    return mod_args


def get_config_file() -> str:
    path_config_file = ""
    while not path_config_file or not Path(path_config_file).exists():
        path_config_file = input(
            f"Enter path of config file (.cfg):\n")
        path_config_file = trim_path_string(
            path_config_file)

        if not Path(path_config_file).exists():
            print(f"This file does not exist! Try again\n")

        if not path_config_file:
            print(f"Please provide a directory\n")
    return path_config_file
