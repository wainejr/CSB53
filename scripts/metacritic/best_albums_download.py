"""Download HTML from metacritic.com for best albums of the year per year"""

from typing import Dict, List, Tuple

from grammy.defines import YEARS_ANALYZE
from grammy.html import download_and_save_html
from grammy.metacritic import get_filename_metacritic_best_albums_year


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
    for year in YEARS_ANALYZE:
        filename = get_filename_metacritic_best_albums_year(year, "html")
        try:
            url, params = get_url_for_year(year)
            download_and_save_html(url, params, filename)
            print(f"Saved year {year}!")
        except Exception as e:
            print(f"Unable to save year {year} :(\nException: {e}")


if __name__ == "__main__":
    main()
