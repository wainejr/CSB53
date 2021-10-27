import os
from datetime import datetime
from typing import Any, List

from bs4 import BeautifulSoup

from grammy.metacritic import (
    InfoMetacritic,
    MetacriticURL,
    get_filename_metacritic_grammy_album_html,
    get_filename_metacritic_grammy_info,
    get_filename_metacritic_grammy_urls_treated,
)


def get_album_info_from_page(page: Any, link_album: str) -> InfoMetacritic:
    artist = (
        page.find("div", class_="product_artist").find("span", class_="band_name").text.strip()
    )
    album = page.find("div", class_="product_title").find("h1").text.strip()
    # Format as Jun 30. 2017
    release_date = (
        page.find("div", class_="product_data")
        .find("li", class_="summary_detail release")
        .find("span", class_="data")
        .text
    )
    release_date = datetime.strptime(release_date, "%b %d, %Y")

    # Full link, as "https://static.metacritic.com/images/products/music/9/a3556781d32c32679cf702fe517c67c5-98.jpg"
    link_img = page.find("img", class_="product_image")["src"]  # only image in tr

    # Format as "87"
    metascore = (
        page.find("div", class_="metascore_wrap")
        .find("div", class_="metascore_w")
        .find("span")
        .text.strip()
    )
    metascore = int(metascore)

    # Format as "8.7"
    userscore = (
        page.find("div", class_="userscore_wrap").find("div", class_="metascore_w").text.strip()
    )
    userscore = int(float(userscore) * 10)  # set same format as metascore

    info = InfoMetacritic(
        artist=artist,
        album=album,
        release_date=release_date,
        userscore=userscore,
        metascore=metascore,
        link_album=link_album,
        link_img=link_img,
    )
    return info


def scrap_info_from_album_page(html_str: str, url: str) -> List[InfoMetacritic]:
    soup = BeautifulSoup(html_str, "lxml")
    album_info = get_album_info_from_page(soup, url)
    return album_info


def main():
    filename = get_filename_metacritic_grammy_urls_treated("csv")
    metacritic_urls = MetacriticURL.read_from_csv(filename)
    total = len(metacritic_urls)
    no_html = 0

    all_metacritic_info: List[InfoMetacritic] = []
    for metacritic_url in metacritic_urls:
        url = metacritic_url.url
        filename_html = get_filename_metacritic_grammy_album_html(url)
        if not os.path.exists(filename_html):
            print(f"'{metacritic_url.artist} - {metacritic_url.album}' does not have html")
            no_html += 1
            continue
        with open(filename_html, "r", encoding="utf-8") as f:
            info_metacritic = scrap_info_from_album_page(f.read(), url)
        all_metacritic_info.append(info_metacritic)

    filename_info = get_filename_metacritic_grammy_info("csv")
    InfoMetacritic.save_to_csv(all_metacritic_info, filename_info)

    print()
    print(f"Not found html for {no_html} albums out of {total}")


if __name__ == "__main__":
    main()
