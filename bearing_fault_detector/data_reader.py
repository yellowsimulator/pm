import yaml
from glob import glob
import pandas as pd


def get_metadata(meta_path: str, exp_nb: int) -> dict:
    """Returns experiment metadata.

    Args:
        meta_path: path to metadata yaml file.
        exp_nb: Experiment number

    Returns:
        exp_nb: experiment metadata.
    """
    with open(f"{meta_path}", "r") as f:
        metadata = yaml.full_load(f)
        exp_meta = metadata.get(f"experiment{exp_nb}")
        return exp_meta


def get_bearing_signal(file_path: str, meta_path: str,
                       exp_nb: int, bearing_nb: int):
    """Returns bearing data.

    Args:
        files_path: bearing data files path.
        meta_path: metadata file path.
        exp_nb: experiment number.
        bearing_nb: bearing number (1, 2, 3 or 4)

    Returns:
        [type]: [description]
    """
    meta = get_metadata(meta_path, exp_nb)
    df = pd.read_csv(file_path, header=None, sep="\t")
    bearing_cols = meta["channel"].get(f"bearing{bearing_nb}")
    sampling_freq = meta.get("sampling_rate_in_Hz")
    bearing_data = df[bearing_cols]
    return bearing_data, sampling_freq






if __name__ == "__main__":
    exp_nb = "1"
    meta_path = "metadata.yaml"
    files_path = f"../data/IMS/{exp_nb}/**"
    bearing_nb = 4
    get_bearing_signal(files_path, meta_path, exp_nb, bearing_nb)
        
