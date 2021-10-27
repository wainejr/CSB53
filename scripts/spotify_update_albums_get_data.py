from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Tuple

import pandas as pd
from pandas import DataFrame

from grammy.billboard import get_filename_billboard_data_all_years
from grammy.defines import CSV_QUOTE, CSV_SEP, GRAMMY_CSV_PATH, YEARS_ANALYZE
from grammy.grammy import InfoGrammy
from grammy.metacritic import get_filename_metacritic_data_all_years
from grammy.spotify import get_filename_spotify_search_albums
from grammy.utils import create_folders_for_file

# Number of billboard album to get info per year
BILLBOARD_album_PER_YEAR = 50
# Number of metacritic album to get info per year
METACRITIC_album_PER_YEAR = 50


@dataclass
class AlbumSearchSpotify:
    album: str
    artist: str

    def __hash__(self) -> int:
        return hash((self.album.lower(), self.artist.lower()))

    def to_csv_row(self) -> Tuple:
        return tuple((self.artist, self.album))

    @classmethod
    def build_from_other(cls, other: Any) -> AlbumSearchSpotify:
        return AlbumSearchSpotify(album=other.album, artist=other.artist)

    @classmethod
    def save_csv(cls, filename: str, albums: List[AlbumSearchSpotify]):
        all_albums_tuples = [a.to_csv_row() for a in albums]
        df: DataFrame = DataFrame.from_records(all_albums_tuples, columns=["artist", "album"])
        df.sort_values(by=["artist", "album"], inplace=True)
        # print(df.head())
        create_folders_for_file(filename)
        df.to_csv(filename, sep=CSV_SEP, quotechar=CSV_QUOTE, encoding="utf-8", index=False)


def get_billboard_albums_to_get_data() -> List[AlbumSearchSpotify]:
    filename = get_filename_billboard_data_all_years("csv")
    df = pd.read_csv(filename, encoding="utf-8", sep=CSV_SEP, quotechar=CSV_QUOTE)
    df["year"] = pd.to_datetime(df["year"], format="%Y")
    all_dfs = []
    for year in YEARS_ANALYZE:
        album_year = df.loc[df["year"].dt.year == year]
        album_get = album_year.loc[df["rank"] <= BILLBOARD_album_PER_YEAR]
        all_dfs.append(album_get.copy(deep=False))
    final_df: DataFrame = pd.concat(all_dfs)

    all_albums: List[AlbumSearchSpotify] = []
    album_column = list(final_df.columns).index("album")
    artist_column = list(final_df.columns).index("artist")
    for f in final_df.values:
        album_search = AlbumSearchSpotify(album=f[album_column], artist=f[artist_column])
        all_albums.append(album_search)
    return all_albums


def get_metacritic_albums_to_get_data() -> List[AlbumSearchSpotify]:
    filename = get_filename_metacritic_data_all_years("csv")
    df = pd.read_csv(filename, encoding="utf-8", sep=CSV_SEP, quotechar=CSV_QUOTE)
    df["release_date"] = pd.to_datetime(df["release_date"], format="%Y-%m-%d")
    all_dfs = []
    for year in YEARS_ANALYZE:
        album_year = df.loc[df["release_date"].dt.year == year]
        album_year.sort_values(by=["metascore", "userscore"])
        album_get = album_year.iloc[:METACRITIC_album_PER_YEAR]
        all_dfs.append(album_get.copy(deep=False))
    final_df: DataFrame = pd.concat(all_dfs)

    all_albums: List[AlbumSearchSpotify] = []
    album_column = list(final_df.columns).index("album")
    artist_column = list(final_df.columns).index("artist")
    for f in final_df.values:
        album_search = AlbumSearchSpotify(album=f[album_column], artist=f[artist_column])
        all_albums.append(album_search)
    return all_albums


def get_grammy_albums_to_get_data() -> List[AlbumSearchSpotify]:
    album = InfoGrammy.read_from_csv(GRAMMY_CSV_PATH)
    return [AlbumSearchSpotify.build_from_other(a) for a in album]


def join_albums(*albums):
    set_albums = set()
    for album in albums:
        set_albums |= set(album)
    return set_albums


def main():
    billboard_albums = get_billboard_albums_to_get_data()
    metacritic_albums = get_metacritic_albums_to_get_data()
    grammy_albums = get_grammy_albums_to_get_data()
    all_albums = join_albums(*[billboard_albums, metacritic_albums, grammy_albums])
    filename = get_filename_spotify_search_albums("csv")
    AlbumSearchSpotify.save_csv(filename, all_albums)


if __name__ == "__main__":
    main()
