import csv
from datetime import datetime
from typing import Any, List

from bs4 import BeautifulSoup

from grammy.defines import YEARS_ANALYZE
from grammy.metacritic import (
    InfoMetacritic,
    get_filename_metacritic_best_albuns_year,
    get_filename_metacritic_data_all_years,
    get_filename_metacritic_data_year,
)
from grammy.utils import create_folders_for_file


def save_csv_info_year(info: List[InfoMetacritic], year: int):
    filename_year = get_filename_metacritic_data_year(year, "csv")
    InfoMetacritic.save_to_csv(info, filename_year)


def join_all_years_data():
    all_info = []
    for year in YEARS_ANALYZE:
        filename_year = get_filename_metacritic_data_year(year, "csv")
        info_year = InfoMetacritic.read_from_csv(filename_year)
        all_info.extend(info_year)
    filename_all_years = get_filename_metacritic_data_all_years("csv")
    create_folders_for_file(filename_year)
    InfoMetacritic.save_to_csv(all_info, filename_all_years)


def read_html_from_year(year: int) -> str:
    filename = get_filename_metacritic_best_albuns_year(year, "html")
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def get_album_info_from_tr(tr: Any) -> InfoMetacritic:
    # Example of link with list of albuns
    # https://www.metacritic.com/browse/albums/score/metascore/year/filtered

    # Full link, as "https://static.metacritic.com/images/products/music/9/a3556781d32c32679cf702fe517c67c5-98.jpg"
    link_img = tr.find("img")["src"]  # only image in tr
    # Link relative to metacritic site, as "/music/stankonia/outkast"
    link_album = tr.find("a", class_="title")["href"]
    link_album = "https://www.metacritic.com" + link_album  # add full link
    # Format as "87"
    metascore = (
        tr.find("div", class_="clamp-metascore").find("div", class_="metascore_w").text.strip()
    )
    metascore = int(metascore)
    # Format as "8.7"
    userscore = (
        tr.find("div", class_="clamp-userscore").find("div", class_="metascore_w").text.strip()
    )
    # When data is not present, it is "tbd"
    if userscore == "tbd":
        userscore = None
    else:
        userscore = int(float(userscore) * 10)  # to int and same sace as metascore
    # Format as "by Outkast"
    artist = tr.find("div", class_="artist").text.strip()
    artist = artist[3:]  # Remove "by "
    album_name = tr.find("a", class_="title").find("h3").text.strip()
    # Format as "October 31, 2000"
    release_date = tr.find("div", class_="clamp-details").find("span").text.strip()
    release_date = datetime.strptime(release_date, "%B %d, %Y")
    # Format as "1."
    place = tr.find("span", class_="title numbered").text.strip()
    place = int(place[:-1])  # remove "." and to int

    info = InfoMetacritic(
        artist=artist,
        album=album_name,
        release_date=release_date,
        userscore=userscore,
        metascore=metascore,
        link_album=link_album,
        link_img=link_img,
    )
    return info


def scrap_info_from_year(year: int) -> List[InfoMetacritic]:
    text = read_html_from_year(year)
    soup = BeautifulSoup(text, "lxml")

    def get_divs_data() -> List[Any]:
        albuns_divs = soup.find_all("div", class_="browse_list_wrapper")
        return albuns_divs

    all_albuns_info: List[InfoMetacritic] = []
    for div in get_divs_data():
        # Get tr that do not hava "spacer" in its class
        albuns_tr_in_div = [
            tr
            for tr in div.find_all("tr")
            if not ("class" in tr.attrs and "spacer" in tr.attrs["class"])
        ]

        for album_tr in albuns_tr_in_div:
            album_info = get_album_info_from_tr(album_tr)
            all_albuns_info.append(album_info)
    return all_albuns_info


def main():
    n_albuns = 0
    for year in YEARS_ANALYZE:
        try:
            info_year = scrap_info_from_year(year)
            n_albuns += len(info_year)
            save_csv_info_year(info_year, year)
            print(f"Processed year {year}! There were {len(info_year)} albuns")
        except Exception as e:
            print(f"Unable to process year {year} :(\nException: {e}")
    join_all_years_data()
    print(f"Joined all albuns! Total of {n_albuns} albuns")


if __name__ == "__main__":
    main()
