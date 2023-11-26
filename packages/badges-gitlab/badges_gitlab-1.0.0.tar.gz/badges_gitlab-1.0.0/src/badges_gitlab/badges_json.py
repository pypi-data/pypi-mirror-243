"""This modules has functions to manipulate and generate standardized json files."""
import json
import os
from pathlib import Path
from typing import Any, TextIO

# Author: Felipe P. Silva
# E-mail: felipefoz@gmail.com


def validate_json_path(directory_path: Any) -> None:
    """Validate destination path if there are any json files.

    Args:
        directory_path (Any): destination path to check
    """
    if os.path.isdir(directory_path) and any(
        File.endswith(".json") for File in os.listdir(directory_path)
    ):
        print("Invalid Directory or no JSON files found in the directory")


def print_json(label: str, message: str, color: str) -> dict:
    """Returns a JSON (Dict) in the format used by shields.io to create badges.

    Args:
        label (str): label for the badge
        message (str): message in the badge
        color (str): color of the badge

    Returns:
        dict: final dictionary version with all fields.
    """
    payload = {"schemaVersion": 1, "label": label, "message": message, "color": color}
    return payload


def json_badge(directory_path, filename: str, json_string: dict) -> None:
    """Write to JSON file to disk to the specified directory.

    Args:
        directory_path (_type_): destination directory
        filename (str): destination json filename
        json_string (dict): dictionary to be converted to json
    """
    print("Creating JSON Badge file for", json_string["label"], "...", end=" ")
    # Using Path function for a platform independent code
    directory_path = Path(directory_path)
    filename = filename + ".json"
    file_to_write = directory_path / filename
    # Write to json file
    outfile: TextIO
    with open(file_to_write, "w", encoding="utf-8") as outfile:
        json.dump(json_string, outfile)
    outfile.close()
    print("Done!")
