from __future__ import annotations

import csv
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional

from grammy.defines import DATA_PATH, DOWNLOAD_PATH
from grammy.utils import create_folders_for_file

BILLBOARD_BEST_ALBUMS = {
    "best_albums_path": os.path.join(DOWNLOAD_PATH, "billboard"),
    "data_path": os.path.join(DATA_PATH, "billboard"),
}


@dataclass
class InfoBillboard:
    artist: str
    album: str
    link_img: str
    rank:int

    @classmethod
    def csv_header(self) -> List[str]:
        return [
            "artist",
            "album",
            "link_img",
            "rank"
        ]

    @property
    def csv_list(self) -> List[Any]:
        return [
            self.artist,
            self.album,
            self.link_img,
            self.rank
        ]

    @classmethod
    def build_info_from_csv(cls, csv_row: List[str]) -> InfoBillboard:
        artist, album = csv_row[0], csv_row[1]
        link_img = csv_row[2]
        rank = int(csv_row[3])
        return InfoBillboard(
            artist=artist,
            album=album,
            link_img=link_img,
            rank=rank
        )

    @classmethod
    def save_to_csv(cls, list_info: List[InfoBillboard], filename: str):
        create_folders_for_file(filename)
        with open(filename, "w", newline="") as csvfile:
            spamwriter = csv.writer(
                csvfile, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL
            )
            spamwriter.writerow(cls.csv_header())
            spamwriter.writerows((info.csv_list for info in list_info))

    @classmethod
    def read_from_csv(cls, filename: str) -> List[InfoBillboard]:
        all_info: List[InfoBillboard] = []
        with open(filename, "r", newline="") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=";", quotechar="|")
            # Skip header
            next(spamreader, None)
            for row in spamreader:
                info = cls.build_info_from_csv(row)
                all_info.append(info)
        return all_info


def get_filename_billboard_best_albums_year(year: int, ext: str) -> str:
    return os.path.join(BILLBOARD_BEST_ALBUMS["best_albums_path"], f"billboard_best_albums_{year}.{ext}")


def get_filename_billboard_data_year(year: int, ext: str) -> str:
    return os.path.join(BILLBOARD_BEST_ALBUMS["data_path"], f"billboard_scrap_year_{year}.{ext}")


def get_filename_billboard_data_all_years(ext: str) -> str:
    return os.path.join(BILLBOARD_BEST_ALBUMS["data_path"], f"all_years.{ext}")
