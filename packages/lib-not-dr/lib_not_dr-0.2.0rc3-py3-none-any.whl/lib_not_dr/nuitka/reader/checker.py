#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import sys

from pathlib import Path
from typing import TYPE_CHECKING


def pyproject_toml(toml_data: dict) -> dict:
    """
    :param toml_data: dict (from pyproject/ raw dict)
    :return: dict
    """
    if "tool" not in toml_data:
        raise ValueError(f"No tool section in config file/dict")

    if "lndl" not in toml_data["tool"]:
        raise ValueError(f"No lib-not-dr(lndl) section in config file/dict")

    if "nuitka" not in toml_data["tool"]["lndl"]:
        raise ValueError(f"No lib-not-dr(lndl).nuitka section in config file/dict")

    nuitka_config = toml_data["tool"]["lndl"]["nuitka"]

    if "main" not in nuitka_config:
        raise ValueError(
            "'main' not define in lib-not-dr(lndl).nuitka section\ndefine it with 'main = [<main.py>]'"
        )

    return nuitka_config


def toml_path_cli() -> Path:
    """
    get toml path from cli args
    :return: Path
    """
    if len(sys.argv) < 2:
        raw_path = Path().cwd()
    else:
        raw_path = Path(sys.argv[1])
    if raw_path.is_file():
        return raw_path

    elif raw_path.is_dir():
        if (raw_path / "pyproject.toml").exists():
            return raw_path / "pyproject.toml"
        else:
            raise FileNotFoundError(f"pyproject.toml not found in {raw_path}")
    else:
        raise FileNotFoundError(f"{raw_path} not found")
