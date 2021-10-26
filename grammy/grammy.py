from __future__ import annotations

import csv
from dataclasses import dataclass
from typing import List


@dataclass
class InfoGrammy:
    year: int
    won: bool
    album: str
    artist: str

    @classmethod
    def build_info_from_csv(cls, csv_row: List[str]) -> InfoGrammy:
        year = int(csv_row[0])
        won = bool(int(csv_row[1]))
        album = csv_row[2]
        artist = csv_row[3]
        return InfoGrammy(
            year=year,
            won=won,
            album=album,
            artist=artist,
        )

    @classmethod
    def read_from_csv(cls, filename: str) -> List[InfoGrammy]:
        all_info: List[InfoGrammy] = []
        with open(filename, "r", newline="", encoding="utf-8") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=";", quotechar="|")
            # Skip header
            next(spamreader, None)
            for row in spamreader:
                info = cls.build_info_from_csv(row)
                all_info.append(info)
        return all_info
