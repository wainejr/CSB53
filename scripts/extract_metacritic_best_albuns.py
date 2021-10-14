from datetime import datetime
from typing import Any, List

from bs4 import BeautifulSoup

from grammy.defines import YEARS_ANALYZE
from grammy.metacritic import InfoMetacritic, get_filename_metacritic_best_albuns_year


def save_csv_info_year(info: List[InfoMetacritic], year: int):
    ...


def read_html_from_year(year: int) -> str:
    filename = get_filename_metacritic_best_albuns_year(year, "html")
    with open(filename, "r") as f:
        return f.read()


def get_album_info_from_tr(tr: Any) -> InfoMetacritic:
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

        def get_albuns_tr_in_div() -> List[Any]:
            # Not get tr spacer classes
            albuns_tr = [
                tr
                for tr in div.find_all("tr")
                if not ("class" in tr.attrs and "spacer" in tr.attrs["class"])
            ]
            return albuns_tr

        for album_tr in get_albuns_tr_in_div():
            album_info = get_album_info_from_tr(album_tr)
            all_albuns_info.append(album_info)
    return all_albuns_info


def main():
    for year in YEARS_ANALYZE:
        info = scrap_info_from_year(year)
        save_csv_info_year(info, year)


if __name__ == "__main__":
    main()
