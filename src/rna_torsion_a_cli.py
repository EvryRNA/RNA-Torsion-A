import argparse
import os.path
from typing import Optional, List

from src.dssr_helper.angles_helper_dssr import AnglesHelperDSSR
from src.mae.mae_helper import MAEHelper
from src.rna_torsionBERT_helper import RNATorsionBERTHelper
from loguru import logger
import numpy as np
import pandas as pd
import tqdm


class RNATorsionACLI:
    def __init__(
        self,
        in_pdb: str,
        out_path: Optional[str],
        *args,
        **kwargs,
    ):
        self.list_files = self._init_pdb(in_pdb)
        self.out_path = out_path

    def _init_pdb(self, in_pdb: Optional[str]) -> List:
        """
        Initialise the inputs structures.
        :param in_pdb: a path to either a .pdb file or a directory of .pdb files
        :return: a list of path to .pdb files
        """
        if os.path.isdir(in_pdb):
            list_files = os.listdir(in_pdb)
            list_files = [os.path.join(in_pdb, file_) for file_ in list_files]
        elif os.path.isfile(in_pdb):
            list_files = [in_pdb]
        else:
            logger.info(f"NO INPUTS FOUND FOR INPUT .PDB: {in_pdb}")
        return list_files

    def run(self):
        all_scores = {"RNA": [], "RNA-Torsion-A": []}
        for in_path in tqdm.tqdm(self.list_files):
            score = self.compute_rna_torsion_a(in_path)
            all_scores["RNA"].append(os.path.basename(in_path))
            all_scores["RNA-Torsion-A"].append(score)
        all_scores = pd.DataFrame(
            all_scores, columns=["RNA-Torsion-A", "RNA"]
        ).set_index("RNA")
        if self.out_path is not None:
            logger.info(f"Saved the output to {self.out_path}")
            all_scores.to_csv(self.out_path, index=True)
        return all_scores

    def compute_rna_torsion_a(self, in_pdb: str) -> float:
        """
        Compute the RNA-Torsion-A scoring function from a .pdb file
        It computes the angles with DSSR, and compute the MAE with the angles predictions from RNA-Torsion-BERT
        :param in_pdb: path to a .pdb file
        :return: the RNA-Torsion-A score
        """
        angles_helper_dssr = AnglesHelperDSSR()
        name, dssr_output = angles_helper_dssr.convert_pdb_file_to_angles(in_pdb)
        sequence = dssr_output["sequence"]
        experimental_angles = dssr_output["angles"]
        torsionBERT_helper = RNATorsionBERTHelper()
        torsionBERT_output = torsionBERT_helper.predict(sequence)
        mae_per_angle = MAEHelper.compute_mae_from_dict(
            experimental_angles, torsionBERT_output
        )
        mae = np.mean(list(mae_per_angle.values()))
        return mae

    @staticmethod
    def get_args():
        parser = argparse.ArgumentParser(
            description="Prediction of Torsional angles for RNA structures"
        )
        # Add command line arguments
        parser.add_argument(
            "--in_pdb",
            dest="in_pdb",
            type=str,
            help="Path a .pdb file or a directory of .pdb files.",
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
    args = RNATorsionACLI.get_args()
    rna_torsionBERT_cli = RNATorsionACLI(**vars(args))
    rna_torsionBERT_cli.run()
