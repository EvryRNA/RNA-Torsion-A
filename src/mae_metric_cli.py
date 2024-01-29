import argparse
import os.path
from typing import Optional, List

from src.dssr_helper.angles_helper_dssr import AnglesHelperDSSR
from src.mae.mae_helper import MAEHelper
from loguru import logger
import numpy as np
import pandas as pd
import tqdm


class MAEMetricCLI:
    def __init__(
        self,
        pred_path: str,
        native_path: str,
        out_path: Optional[str],
        *args,
        **kwargs,
    ):
        self.pred_paths = self._init_pred_path(pred_path)
        self.native_path = native_path
        self.out_path = out_path

    def _init_pred_path(self, pred_path: str) -> List:
        """
        Initialise the inputs structures.
        :param pred_path: path to a .pdb file or a directory of .pdb files
        :return: list with full path for each .pdb file
        """
        pred_paths = []
        if os.path.isdir(pred_path):
            pred_paths.extend(
                [
                    os.path.join(pred_path, file_)
                    for file_ in os.listdir(pred_path)
                    if file_.endswith(".pdb")
                ]
            )
        elif os.path.isfile(pred_path):
            pred_paths.append(pred_path)
        else:
            logger.info(f"NO INPUTS FOUND FOR INPUT .PDB: {pred_path}")
        return pred_paths

    def run(self):
        all_scores = {"RNA": [], "MAE": []}
        for pred_path in tqdm.tqdm(self.pred_paths):
            score = self.compute_mae_metric(pred_path, self.native_path)
            all_scores["RNA"].append(os.path.basename(pred_path))
            all_scores["MAE"].append(score)
        all_scores = pd.DataFrame(all_scores, columns=["MAE", "RNA"]).set_index("RNA")
        if self.out_path is not None:
            logger.info(f"Saved the output to {self.out_path}")
            all_scores.to_csv(self.out_path, index=True)
        return all_scores

    def compute_mae_metric(self, pred_path: str, native_path: str) -> float:
        """
        Compute the MAE between the true angles and the angles from the predicted structure
        :param pred_path: path to a .pdb file of a predicted structure
        :param native_path: path to the native structure
        :return: the MAE averaged over all the angles
        """
        angles_helper_dssr = AnglesHelperDSSR()
        _, true_angles = angles_helper_dssr.convert_pdb_file_to_angles(native_path)
        _, pred_angles = angles_helper_dssr.convert_pdb_file_to_angles(pred_path)
        true_angles, pred_angles = {"name": true_angles}, {"name": pred_angles}
        mae_per_angle = MAEHelper.compute_mae_from_dict(pred_angles, true_angles)
        mae = np.mean(list(mae_per_angle.values()))
        return mae

    @staticmethod
    def get_args():
        parser = argparse.ArgumentParser(
            description="Prediction of Torsional angles for RNA structures"
        )
        # Add command line arguments
        parser.add_argument(
            "--pred_path",
            dest="pred_path",
            type=str,
            help="Path a .pdb file or a directory of .pdb files of predicted structures.",
            default=None,
        )
        parser.add_argument(
            "--native_path",
            dest="native_path",
            type=str,
            help="Path a .pdb file of the reference native structure.",
            default=None,
        )
        parser.add_argument(
            "--out_path",
            dest="out_path",
            type=str,
            help="Path to a .csv file to save the predictions.",
            default=None,
        )
        # Parse the command line arguments
        args = parser.parse_args()
        return args


if __name__ == "__main__":
    args = MAEMetricCLI.get_args()
    mae_helper_cli = MAEMetricCLI(**vars(args))
    mae_helper_cli.run()
