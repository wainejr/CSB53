import json
from typing import Dict, List, Optional

import pandas as pd

from grammy.billboard import InfoBillboard
from grammy.defines import CSV_QUOTE, CSV_SEP
from grammy.metacritic import InfoMetacritic

FILE_ALL_ALBUMS = "data/metacritic/all_albums_data.json"

FILE_METACRITIC_ALBUMS = "data/metacritic/all_years.csv"

FILE_GRAMMY_ALBUMS = "data/grammy/albums_of_the_year.csv"
FILE_GRAMMY_URLS = "data/metacritic/grammies_urls_treated.csv"

FILE_BILLBOARD_ALBUMS = "data/billboard/all_years.csv"
FILE_BILLBOARD_URLS = "data/metacritic/billboard_urls_treated.csv"

FILE_OUTPUT = "data/all_data.json"


def get_all_albums_data() -> List[Dict]:
    with open(FILE_ALL_ALBUMS, "r", encoding="utf-8") as f:
        return json.load(f)


def get_csv_df(filename: str):
    return pd.read_csv(filename, sep=CSV_SEP, quotechar=CSV_QUOTE, encoding="utf-8")


def get_grammy_df() -> pd.DataFrame:
    albums = get_csv_df(FILE_GRAMMY_ALBUMS)
    albums_url = get_csv_df(FILE_GRAMMY_URLS)
    # Add url column
    albums["url"] = None
    # Add url to all albums in data
    for album_url in albums_url.values:
        artist, album, url = album_url
        albums.loc[(albums["artist"] == artist) & (albums["album"] == album), "url"] = url

    return albums


def get_billboard_df() -> pd.DataFrame:
    albums = get_csv_df(FILE_BILLBOARD_ALBUMS)
    albums_url = get_csv_df(FILE_BILLBOARD_URLS)
    # Add url column
    albums["url"] = None
    # Add url to all albums in data
    for album_url in albums_url.values:
        artist, album, url = album_url
        albums.loc[(albums["artist"] == artist) & (albums["album"] == album), "url"] = url

    return albums


def get_billboard_album_data(url: str, billboard_df: pd.DataFrame) -> Optional[Dict]:
    billboard_album_data = billboard_df.loc[billboard_df["url"] == url].values.tolist()
    if len(billboard_album_data) == 0:
        return None
    header = InfoBillboard.csv_header()
    indexes = [header.index(n) for n in ["year", "rank"]]
    data_ret = {}
    for b_album in billboard_album_data:
        # year, rank
        data_ret[b_album[indexes[0]]] = b_album[indexes[1]]
    return data_ret


def get_grammy_album_data(url: str, grammy_df: pd.DataFrame) -> Optional[Dict]:
    grammy_album_data = grammy_df.loc[grammy_df["url"] == url].values.tolist()
    # Only one album
    if len(grammy_album_data) > 0:
        if len(grammy_album_data) > 1:
            raise ValueError(f"this is wrong man, {grammy_album_data}")
        grammy_album_data = grammy_album_data[0]
    else:
        return None
    headers = ["year", "won", "album", "artist"]
    indexes = [0, 1]
    data_ret = {headers[i]: grammy_album_data[i] for i in indexes}
    return data_ret


def main():
    grammy_df = get_grammy_df()
    billboard_df = get_billboard_df()

    all_albums = get_all_albums_data()
    for album in all_albums:
        url = album["link_album"]
        album["grammy"] = get_grammy_album_data(url, grammy_df)
        album["billboard"] = get_billboard_album_data(url, billboard_df)

    with open(FILE_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(all_albums, f, ensure_ascii=False)


if __name__ == "__main__":
    main()
