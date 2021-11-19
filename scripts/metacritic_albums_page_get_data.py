from __future__ import annotations

import os
from typing import Any, List, Dict
from datetime import datetime
import json
import time

import pandas as pd
from pandas import DataFrame
from bs4 import BeautifulSoup


def get_album_info_from_page(page: Any, link_album: str) -> Dict:
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
    release_date = str(release_date)

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

    try:
        # Format as "8.7"
        userscore = (
            page.find("div", class_="userscore_wrap")
            .find("div", class_="metascore_w")
            .text.strip()
        )
        userscore = int(float(userscore) * 10)  # set same format as metascore
    except:
        userscore = None
    try:
        genres = page.find("li", class_="product_genre").find_all("span")
        genres = [g.text for g in genres if not g.text.lower().startswith("genre")]
    except:
        genres = None

    info = dict(
        artist=artist,
        album=album,
        release_date=release_date,
        userscore=userscore,
        metascore=metascore,
        link_album=link_album,
        link_img=link_img,
        genres=genres,
    )
    return info


def scrap_info_from_album_page(html_str: str, url: str) -> Dict:
    soup = BeautifulSoup(html_str, "lxml")
    album_info = get_album_info_from_page(soup, url)
    return album_info


def main():
    filename_save = "data/metacritic/all_albums_data.json"
    base_html_path = "downloads/grammy_metacritic/"
    all_albums_dict: List[Dict] = []
    unable_to_get = []
    all_html_files = os.listdir(base_html_path)
    t0 = time.time()

    for i, file in enumerate(all_html_files):
        if i % 100 == 0 and i != 0:
            print(f"Processed {i} out of {len(all_html_files)}. Total time: {time.time()-t0:.2f} ")

        filename_html = os.path.join(base_html_path, file)
        with open(filename_html, "r", encoding="utf-8") as f:
            html_str = f.read()
            # Remove .html, then join _
        url = "https://www.metacritic.com/music/" + "/".join(file[:-5].split("_"))
        try:
            data = scrap_info_from_album_page(html_str, url)
            all_albums_dict.append(data)
        except Exception as e:
            unable_to_get.append(file)
            print(f"Unable to get data from {file}, {e}")

    print(f"Unable to get data from {len(unable_to_get)} out of {len(all_html_files)}")
    print(all_albums_dict[0])
    with open(filename_save, "w", encoding="utf-8") as f:
        json.dump(all_albums_dict, f, ensure_ascii=False)


if __name__ == "__main__":
    main()
