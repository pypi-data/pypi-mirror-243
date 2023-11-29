from typing import List, Tuple
from pathlib import Path
from .constants import BashColors as bc
from colorama import just_fix_windows_console
just_fix_windows_console()

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
            f"{bc.UYellow}Enter path of config file (.cfg):{bc.Reset}\n")
        path_config_file = trim_path_string(
            path_config_file)

        if not Path(path_config_file).exists():
            print(f"{bc.BRed}This file does not exist! Try again{bc.Reset}\n")

        if not path_config_file:
            print(f"{bc.BRed}Please provide a directory{bc.Reset}\n")
    return path_config_file


def make_uyellow_newline(string: str) -> str:
    return f"{bc.UYellow}string{bc.Reset}\n"

def make_bred_newline(string: str) -> str:
    return f"{bc.BRed}string{bc.Reset}\n"