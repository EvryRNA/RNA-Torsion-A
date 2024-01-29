import json
from typing import Dict
import numpy as np


def save_json(content: Dict, path: str):
    """Save the dictionary into a json file.
    Args
    :param content: the object to save
    :param path: the path where to save. Could have .json or not in the path
    """
    assert type(content) is dict
    if path.endswith(".json"):
        path_to_save = path
    else:
        path_to_save = path + ".json"
    with open(path_to_save, "w") as file:
        json.dump(content, file)


def read_json(path: str, to_clean: bool = False) -> Dict:
    """Read the json file.
    Args
    :param path: the path to the file
    :param to_clean: whether to clean the angles or not
    :return a dictionary of the json file
    """
    if path.endswith(".json"):
        with open(path, "rb") as f:
            content = json.loads(f.read())
            if to_clean:
                return convert_angles_string_to_float(content)
            return content
    else:
        print("Not a json file")
        return {}


def convert_angles_string_to_float(angles: Dict):
    """
    Convert the string to float and replace the NA values by np.nan
    """
    clean_angles = angles.copy()
    for rna_name, rna in angles.items():
        for angle_name, angles in rna["angles"].items():
            new_angles = [
                float(angle) if angle not in ["NA", None, "", "BII", "BI"] else np.nan
                for angle in angles
            ]
            clean_angles[rna_name]["angles"][angle_name] = new_angles
    return clean_angles
