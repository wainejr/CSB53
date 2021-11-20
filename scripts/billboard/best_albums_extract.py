import csv
from datetime import datetime
from typing import Any, List

from bs4 import BeautifulSoup

from grammy.billboard import (
    InfoBillboard,
    get_filename_billboard_best_albums_year,
    get_filename_billboard_data_all_years,
    get_filename_billboard_data_year,
)
from grammy.defines import YEARS_ANALYZE
from grammy.utils import create_folders_for_file


def save_csv_info_year(info: List[InfoBillboard], year: int):
    filename_year = get_filename_billboard_data_year(year, "csv")
    InfoBillboard.save_to_csv(info, filename_year)


def join_all_years_data():
    all_info = []
    for year in YEARS_ANALYZE:
        filename_year = get_filename_billboard_data_year(year, "csv")
        info_year = InfoBillboard.read_from_csv(filename_year)
        all_info.extend(info_year)
    filename_all_years = get_filename_billboard_data_all_years("csv")
    create_folders_for_file(filename_year)
    InfoBillboard.save_to_csv(all_info, filename_all_years)


def read_html_from_year(year: int) -> str:
    filename = get_filename_billboard_best_albums_year(year, "html")
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def get_album_info_from_art(art: Any, year: int) -> InfoBillboard:
    # Example of link with list of albums
    # https://www.billboard.com/charts/year-end/2020/catalog-albums

    # Full link, as 'https://charts-static.billboard.com/img/1999/04/johnny-cash-q0u-16-biggest-hits-hx0-53x53.jpg'
    link_img = art.find("img")["src"]  # only image in art
    # Format as "Guns N' Roses"
    artist = art.find("div", class_="ye-chart-item__artist").text.strip()
    # Format as "Greatest Hits"
    album_name = art.find("div", class_="ye-chart-item__title").text.strip()
    # Format as "1"
    rank = int(art.find("div", class_="ye-chart-item__rank").text.strip())

    info = InfoBillboard(artist=artist, album=album_name, link_img=link_img, rank=rank, year=year)
    return info


def scrap_info_from_year(year: int) -> List[InfoBillboard]:
    text = read_html_from_year(year)
    soup = BeautifulSoup(text, "lxml")

    def get_divs_data() -> List[Any]:
        albums_divs = soup.find_all("div", class_="chart-details__item-list")
        return albums_divs

    all_albums_info: List[InfoBillboard] = []
    for div in get_divs_data():
        albums_article_in_div = [
            article for article in div.find_all("article", class_="ye-chart-item")
        ]
        for album_art in albums_article_in_div:
            album_info = get_album_info_from_art(album_art, year)
            all_albums_info.append(album_info)
    return all_albums_info


def main():
    n_albums = 0
    for year in YEARS_ANALYZE:
        try:
            info_year = scrap_info_from_year(year)
            n_albums += len(info_year)
            save_csv_info_year(info_year, year)
            print(f"Processed year {year}! There were {len(info_year)} albums")
        except Exception as e:
            print(f"Unable to process year {year} :(\nException: {e}")
    join_all_years_data()
    print(f"Joined all albums! Total of {n_albums} albums")


if __name__ == "__main__":
    main()
