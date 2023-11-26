"""Creates standardized badges files using anybadge package.

This function creates the badge svg file from
json file with the shields.io (https://shields.io/endpoint) json format
badge format =
{"schemaVersion":1,"label":"hello","message":"sweet world","color":"orange"}
"""
import json
import os
from pathlib import Path
from typing import Any

import anybadge  # type: ignore

# Author: Felipe P. Silva
# E-mail: felipefoz@gmail.com


def replace_space(string: str) -> str:
    """Replaces any spaces to make it easier to use later as url in badges linking.

    Args:
        string (str): string to evaluate

    Returns:
        str: string without space
    """
    return string.replace(" ", "_")


def validate_json_path(directory_path: Any) -> bool:
    """Check if there is any json files or the directory is valid.

    Args:
        directory_path (Any): destination path to evaluate.

    Returns:
        bool: validation result
    """
    return os.path.isdir(directory_path) and any(
        File.endswith(".json") for File in os.listdir(directory_path)
    )


def print_badges(directory_path: Any) -> None:
    """Print badges from json files.

    Iterates within the directory finding json files and then use
    anybadge pkg to generate them.

    Args:
        directory_path (Any): _description_
    """
    if validate_json_path(directory_path):
        directory_path = Path(directory_path)
        for json_file in os.listdir(Path(directory_path)):
            if json_file.endswith(".json"):
                # Opening JSON file
                full_json_path = os.path.join(directory_path, json_file)
                with open(full_json_path, encoding="utf-8") as file_json:
                    # returns JSON object
                    json_string = json.load(file_json)
                    print("Creating badge for", json_string["label"], "...", end=" ")
                    filename = str(Path(full_json_path).stem) + ".svg"
                    destination_file = directory_path / filename
                    anybadge.Badge(
                        label=json_string["label"],
                        value=json_string["message"],
                        default_color=json_string["color"],
                    ).write_badge(str(destination_file), overwrite=True)
                    print("Done!")
                    # Closing file
    else:
        print("Error: invalid directory or no JSON files found in the directory...")
