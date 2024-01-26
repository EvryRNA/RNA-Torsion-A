"""
Class that defines the useful functions for preprocessing .pdb files to angles.
"""
import argparse
import os
import subprocess
from typing import Optional, Dict, Tuple
import pandas as pd

import tqdm

from src.utils import save_json


class AnglesHelperAbstract:
    def __init__(self, folder_path: Optional[str] = None, *args, **kwargs):
        self.folder_path = folder_path

    def convert_pdb_to_angles(
        self, folder_path: Optional[str] = None, output_path: Optional[str] = None
    ) -> Dict:
        """
        Convert a folder with .pdb files to a json file
        :param folder_path: path to the folder where are stored the .pdb files
        :param output_path: path to save the output in .json
        :return: a json file of the following form:
                {
                    'SimRNA-...' :
                        {
                            'sequence' : 'AUUUGCUU.GU',
                            'angles' :
                                { 'ETA' : [126, ...],
                                  'THETA': [177, ...]
                                }
                        },
                        ...
                }
        """
        folder_path = self.folder_path if folder_path is None else folder_path
        list_files = os.listdir(folder_path)
        outputs = {}
        for file_ in tqdm.tqdm(list_files):
            input_path = os.path.join(folder_path, file_)
            try:
                name, content = self.convert_pdb_file_to_angles(input_path)
                outputs[name] = content
            except ValueError:
                continue
        save_json(outputs, output_path)

    def convert_pdb_file_to_angles(self, input_path: str) -> Tuple[str, Dict]:
        """
        Return the sequence and pseudo-torsion angles from a .pdb file
        :param input_path: the path to a .pdb file
        :return:
        """
        name = os.path.basename(input_path).replace(".pdb", "")
        output = self._get_angles_from_c_code(input_path)
        return name, output

    def get_command(self, input_path) -> str:
        """
        Return the command to launch
        :param input_path: the path to a .pdb file
        :return: os command to execute
        """
        raise NotImplementedError

    def _get_angles_from_c_code(self, input_path: str) -> Dict:
        """
        Run the C++ code to get the angles
        :param input_path: the path to a .pdb file
        :return:
        """
        command = self.get_command(input_path)
        df = self.launch_os_command(command)
        output = self._convert_csv_to_angles(df)
        return output

    def _convert_csv_to_angles(self, df: pd.DataFrame) -> Dict:
        """
        Convert the output csv from code to a sequence with the angles
        :param df: csv file from the code
        :return: dictionary of the form
                { 'sequence' : "AC...",
                   'angles': {
                      'ETA': [163, 58, ...],
                      'THETA' : [177, 23, ...],
                      ...
                    }
                }
        """
        raise NotImplementedError

    def convert_output_to_csv(self, output: str) -> pd.DataFrame:
        """
        Convert the output of command to csv
        """
        raise NotImplementedError

    def launch_os_command(self, command: str) -> pd.DataFrame:
        """
        Launch an OS command
        :param command: the system command to launch
        :return dataframe of the output
        """
        output = subprocess.check_output(command, shell=True)
        return self.convert_output_to_csv(output)

    @staticmethod
    def get_arguments():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--folder_path",
            dest="folder_path",
            type=str,
            default=None,
            help="Path to the folder where are stored the .pdb files",
        )
        parser.add_argument(
            "--output_path",
            dest="output_path",
            type=str,
            default="output.json",
            help="Path to save the output in .json",
        )
        args = parser.parse_args()
        return args
