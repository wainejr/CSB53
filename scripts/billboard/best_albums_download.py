"""Download HTML from billboard.com for best albums of the year per year"""

from typing import Dict, List, Tuple

from grammy.billboard import get_filename_billboard_best_albums_year
from grammy.defines import YEARS_ANALYZE
from grammy.html import download_and_save_html


def get_url_for_year(year: int) -> Tuple[str, Dict[str, str]]:
    url = "https://www.billboard.com/charts/year-end/{0}/top-billboard-200-albums".format(year)
    return url, {}


def main():
    for year in YEARS_ANALYZE:
        filename = get_filename_billboard_best_albums_year(year, "html")
        try:
            url, params = get_url_for_year(year)
            download_and_save_html(url, params, filename)
            print(f"Saved year {year}!")
        except Exception as e:
            print(f"Unable to save year {year} :(\nException: {e}")


if __name__ == "__main__":
    main()
