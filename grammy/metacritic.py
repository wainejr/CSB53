import os
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from grammy.defines import DATA_PATH, DOWNLOAD_PATH

METACRITIC_BEST_ALBUNS = {
    "best_albuns_path": os.path.join(DOWNLOAD_PATH, "metacritic"),
    "data_path": os.path.join(DATA_PATH, "metacritic"),
}


@dataclass
class InfoMetacritic:
    artist: str
    album: str
    release_date: datetime
    userscore: Optional[int]
    metascore: int
    link_album: str
    link_img: str


def get_filename_metacritic_best_albuns_year(year: int, ext: str) -> str:
    return os.path.join(METACRITIC_BEST_ALBUNS["best_albuns_path"], f"best_albuns_{year}.{ext}")


def get_filename_metacritic_data_year(year: int, ext: str) -> str:
    return os.path.join(METACRITIC_BEST_ALBUNS["data_path"], f"scrap_year_{year}.{ext}")


def get_filename_metacritic_data_all_years(ext: str) -> str:
    return os.path.join(METACRITIC_BEST_ALBUNS["data_path"], f"all_years.{ext}")
