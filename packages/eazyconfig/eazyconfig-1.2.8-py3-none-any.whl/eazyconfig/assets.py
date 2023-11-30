import logging
import colorlog
from typing import List
from pathlib import Path
from .constants import BashColors as bc, Format
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
            print(f"{bc.BRed}Please provide a directory!{bc.Reset}\n")
    return path_config_file


def get_input_output_cmdline():
    path_input = ""
    while not path_input or not Path(path_input).exists:
        path_input = trim_path_string(input(
            f"{bc.UYellow}Enter the input directory:{bc.Reset}\n"))
        if not path_input:
            print(f"{bc.BRed}Please enter a directory!{bc.Reset}\n")

        if not Path(path_input).exists:
            print(
                f"{bc.BRed}This directory does NOT exist, please try again!{bc.Reset}\n")

    path_output = ""
    while not path_output or not Path(path_output).exists:
        path_output = trim_path_string(input(
            f"\n{bc.UYellow}Enter the output directory:{bc.Reset}\n"))
        if not path_output:
            print(f"{bc.BRed}Please enter a directory!{bc.Reset}\n")

        if not Path(path_output).exists:
            print(
                f"{bc.BRed}This directory does NOT exist, please try again!{bc.Reset}\n")

    return path_input, path_output


def get_logger(name: str, filename: str, level=logging.INFO):
    logging.basicConfig(
        filename=filename,
        level=level,
        format=Format.file_log.value
    )

    logger = logging.getLogger(name)

    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            Format.stream_log.value,
            datefmt="%Y-%m-%d %H:%M:%S %Z")
    )
    logger.addHandler(handler)
    return logger



def make_uyellow_newline(string: str) -> str:
    return f"{bc.UYellow}{string}{bc.Reset}\n"


def make_bred_newline(string: str) -> str:
    return f"{bc.BRed}{string}{bc.Reset}\n"


def make_bgreen_newline(string: str) -> str:
    return f"{bc.BGreen}{string}{bc.Reset}\n"
