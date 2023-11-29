from typing import List


def trim_path_string(*args) -> List[str] | str:
    mod_args = []
    for arg in args:
        mod_args.append(arg.strip().replace("'", "").replace('"', ''))

    if len(mod_args) == 1:
        return mod_args[0]
    return mod_args