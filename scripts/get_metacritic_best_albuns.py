"""Download HTML from metacritic.com for best albums of the year per year"""

from typing import Dict, List, Tuple

from grammy.defines import get_filename_metacritic_best_albuns
from grammy.html import download_and_save_html

# 2000-2020
YEARS: List[int] = list(range(2000, 2021))


def get_url_for_year(year: int) -> Tuple[str, Dict[str, str]]:
    url = "https://www.metacritic.com/browse/albums/score/metascore/year/filtered"
    params = {
        "year_selected": str(year),
        "sort": "desc",
        "view": "detailed",
        "distribution": "",
    }
    return url, params


def main():
    for year in YEARS:
        filename = get_filename_metacritic_best_albuns(year)
        url, params = get_url_for_year(year)
        download_and_save_html(url, params, filename)
        print(f"Saved year {year}!")


if __name__ == "__main__":
    main()
