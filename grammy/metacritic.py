from __future__ import annotations

import csv
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional

from grammy.defines import CSV_QUOTE, CSV_SEP, DATA_PATH, DOWNLOAD_PATH
from grammy.utils import create_folders_for_file

METACRITIC_BEST_ALBUMS = {
    "best_albums_path": os.path.join(DOWNLOAD_PATH, "metacritic"),
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

    @classmethod
    def csv_header(self) -> List[str]:
        return [
            "artist",
            "album",
            "release_date",
            "userscore",
            "metascore",
            "link_album",
            "link_img",
        ]

    @property
    def csv_list(self) -> List[Any]:
        return [
            self.artist,
            self.album,
            self.release_date.strftime("%Y-%m-%d"),
            self.userscore if self.userscore is not None else "null",
            self.metascore,
            self.link_album,
            self.link_img,
        ]

    @classmethod
    def build_info_from_csv(cls, csv_row: List[str]) -> InfoMetacritic:
        artist, album = csv_row[0], csv_row[1]
        release_date = datetime.strptime(csv_row[2], "%Y-%m-%d")
        userscore = int(csv_row[3]) if csv_row[3] != "null" else None
        metascore = int(csv_row[4])
        link_album, link_img = csv_row[5], csv_row[6]
        return InfoMetacritic(
            artist=artist,
            album=album,
            release_date=release_date,
            userscore=userscore,
            metascore=metascore,
            link_album=link_album,
            link_img=link_img,
        )

    @classmethod
    def save_to_csv(cls, list_info: List[InfoMetacritic], filename: str):
        create_folders_for_file(filename)
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            spamwriter = csv.writer(
                csvfile, delimiter=CSV_SEP, quotechar=CSV_QUOTE, quoting=csv.QUOTE_MINIMAL
            )
            spamwriter.writerow(cls.csv_header())
            spamwriter.writerows((info.csv_list for info in list_info))

    @classmethod
    def read_from_csv(cls, filename: str) -> List[InfoMetacritic]:
        all_info: List[InfoMetacritic] = []
        with open(filename, "r", newline="", encoding="utf-8") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=CSV_SEP, quotechar=CSV_QUOTE)
            # Skip header
            next(spamreader, None)
            for row in spamreader:
                info = cls.build_info_from_csv(row)
                all_info.append(info)
        return all_info


def get_filename_metacritic_best_albums_year(year: int, ext: str) -> str:
    return os.path.join(METACRITIC_BEST_ALBUMS["best_albums_path"], f"best_albums_{year}.{ext}")


def get_filename_metacritic_data_year(year: int, ext: str) -> str:
    return os.path.join(METACRITIC_BEST_ALBUMS["data_path"], f"scrap_year_{year}.{ext}")


def get_filename_metacritic_data_all_years(ext: str) -> str:
    return os.path.join(METACRITIC_BEST_ALBUMS["data_path"], f"all_years.{ext}")
