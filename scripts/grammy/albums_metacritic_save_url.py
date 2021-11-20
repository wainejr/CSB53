from __future__ import annotations

from typing import List

from grammy.defines import GRAMMY_CSV_PATH
from grammy.grammy import InfoGrammy
from grammy.metacritic import MetacriticURL, get_filename_metacritic_grammy_urls


def main():
    grammy_infos = InfoGrammy.read_from_csv(GRAMMY_CSV_PATH)
    all_urls: List[MetacriticURL] = []

    for grammy_info in grammy_infos:
        all_urls.append(
            MetacriticURL.build_from_artist_album(
                artist=grammy_info.artist,
                album=grammy_info.album,
            )
        )
    filename = get_filename_metacritic_grammy_urls("csv")
    MetacriticURL.save_to_csv(filename, all_urls)


if __name__ == "__main__":
    main()
