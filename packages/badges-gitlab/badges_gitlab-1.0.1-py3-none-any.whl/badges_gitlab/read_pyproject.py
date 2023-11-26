"""Read pyproject.toml and import the parameters to be used in the function."""
import os

import toml  # type: ignore
from toml.decoder import TomlDecodeError  # type: ignore


def pyproject_exists(file_path: str) -> bool:
    """Verify if the file exists, used internally.

    Args:
        file_path (str): file path for the pyproject file

    Returns:
        bool: true or false for the operation.
    """
    return os.path.isfile(file_path)


def load_pyproject(file_path: str) -> dict:
    """Load the tool.badges_gitlab section from the toml file.

    Most of the cases it is pyproject.toml because it is hardcoded into main function

    Args:
        file_path (str): path for the pyproject.toml

    Returns:
        dict: dictionary with the configuration
    """
    try:
        loaded_file = toml.load(file_path)
        config_dict = loaded_file["tool"]["badges_gitlab"]
        return config_dict
    except TomlDecodeError:
        print("Incompatible .toml file!")
        return {}
    except KeyError:
        print('The "badges_gitlab" section in pyproject.toml was not found!')
        return {}


def pyproject_config(file_path: str) -> dict:
    """Load pyproject.toml and return the content as dict.

    Args:
        file_path (str): file path for the pyproject

    Returns:
        dict: dictionary with the configuration for the badges_gitlab tool
    """
    if not pyproject_exists(file_path):
        return {}
    # if exists, return the dict
    return load_pyproject(file_path)
