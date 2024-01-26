import os
from typing import Dict

import numpy as np
import pandas as pd

from helper.rna_angles_prediction_dssr.src.dssr_wrapper import DSSRWrapper
from src.dssr_helper.angles_helper_abstract import AnglesHelperAbstract


class AnglesHelperDSSR(AnglesHelperAbstract):
    """
    File that implements the DSSR code.
    It uses a wrapper implementation available at:

    """

    def __init__(
        self,
        dssr_bin_path: str = os.path.join(
            "helper", "rna_angles_prediction_dssr", "dssr", "bin", "analyze"
        ),
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.wrapper = DSSRWrapper(dssr_bin_path)

    def _get_angles_from_c_code(self, input_path: str) -> Dict:
        """
        Run the C++ code to get the angles
        :param input_path: the path to a .pdb file
        :return:
        """
        df = self.wrapper.get_all_angles_from_dssr_one_file(input_path, to_csv=True)
        output = self._convert_csv_to_angles(df)
        return output

    def _convert_csv_to_angles(self, df: pd.DataFrame) -> Dict:
        """
        Convert the CSV to a dictionary
        :param df: output of the C code
        :return: dictionary of the form
                { 'sequence' : "AC...",
                   'angles': {
                      'ETA': [163, 58, ...],
                      'THETA' : [177, 23, ...]
                    }
                }
        """
        angles = [
            "alpha",
            "beta",
            "gamma",
            "delta",
            "epsilon",
            "zeta",
            "chi",
            "eta",
            "theta",
        ]
        output = {"sequence": "".join(df["sequence"].tolist()), "angles": {}}
        for angle in angles:
            replaces = ["None", "NA", "BI", "", "BII"]
            c_angles = df[angle].replace({key: None for key in replaces}).tolist()
            output["angles"][angle] = [
                float(c_angle) if c_angle is not None else np.nan
                for c_angle in c_angles
            ]
        return output


if __name__ == "__main__":
    args = AnglesHelperDSSR.get_arguments()
    angles_helper = AnglesHelperDSSR()
    angles_helper.convert_pdb_to_angles(**vars(args))
