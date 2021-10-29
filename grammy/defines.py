import os
import pathlib
from typing import List

# 2000-2020
YEARS_ANALYZE: List[int] = list(range(2000, 2021))
CSV_SEP = ";"
CSV_QUOTE = "|"

__root_folder = pathlib.Path(__file__).parent.parent.absolute()
DOWNLOAD_PATH = os.path.join(__root_folder, "downloads")
DATA_PATH = os.path.join(__root_folder, "data")
GRAMMY_CSV_PATH = os.path.join(DATA_PATH, "grammy/albums_of_the_year.csv")
