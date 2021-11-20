from __future__ import annotations

from typing import List

from grammy.billboard import InfoBillboard, get_filename_billboard_data_all_years
from grammy.metacritic import MetacriticURL, get_filename_metacritic_billboard_urls


def main():
    filename_read = get_filename_billboard_data_all_years("csv")
    billboard_infos = InfoBillboard.read_from_csv(filename_read)
    all_urls: List[MetacriticURL] = []

    for billboard_info in billboard_infos:
        all_urls.append(
            MetacriticURL.build_from_artist_album(
                artist=billboard_info.artist,
                album=billboard_info.album,
            )
        )
    all_urls = list(set(all_urls))
    filename = get_filename_metacritic_billboard_urls("csv")
    MetacriticURL.save_to_csv(filename, all_urls)


if __name__ == "__main__":
    main()
