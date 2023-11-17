import numpy as np
from scipy.io import readsav

from sun_eruption_detection.consts import SAV_FILES


def read_sav_file(verbose: bool = False) -> np.recarray:
    sav_file = list(SAV_FILES.iterdir())[0]  # TODO -> adjust to read more than one sav file
    sav_content = readsav(str(sav_file), verbose=verbose)
    return sav_content.erupt_str
