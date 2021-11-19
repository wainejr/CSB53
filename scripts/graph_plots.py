import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from matplotlib.ticker import MaxNLocator
from grammy.billboard import get_filename_billboard_data_all_years
from grammy.defines import CSV_QUOTE, CSV_SEP
from grammy.grammy import get_filename_grammy_albums_of_the_year
from grammy.metacritic import (
    get_filename_metacritic_grammy_info,
    get_filename_metacritic_data_all_years,
)


def main():

    grammy_albums_of_the_year_path = get_filename_grammy_albums_of_the_year("csv")
    grammy_albums_of_the_year = pd.read_csv(
        grammy_albums_of_the_year_path, encoding="utf-8", sep=CSV_SEP, quotechar=CSV_QUOTE
    )
    grammy_albums_of_the_year["album"] = grammy_albums_of_the_year["album"].str.lower()

    grammy_albums_path = get_filename_metacritic_grammy_info("csv")
    grammy_albums = pd.read_csv(
        grammy_albums_path, encoding="utf-8", sep=CSV_SEP, quotechar=CSV_QUOTE
    )
    grammy_albums["album"] = grammy_albums["album"].str.lower()

    grammy_albums_merged = pd.merge(grammy_albums_of_the_year, grammy_albums, on="album")
    grammy_albums_merged = grammy_albums_merged.drop(columns=["artist_x"])
    grammy_albums_merged = grammy_albums_merged.rename(columns={"artist_y": "artist"})
    # grammy_albums_merged['mean'] = grammy_albums_merged.groupby('year')['metascore'].transform('mean')
    # grammy_albums_merged['max'] = grammy_albums_merged.groupby('year')['metascore'].transform('max')
    # grammy_albums_merged['min'] = grammy_albums_merged.groupby('year')['metascore'].transform('min')

    # graph 01
    grammy_albums_mean_year = grammy_albums_merged.groupby(["year"]).mean().reset_index()

    # graph 02
    grammy_albums_winners = grammy_albums_merged.loc[grammy_albums_merged["won"] == 1]

    # ----------------------------------------------------------------------------------------
    # graph 3.1 - NOT READY
    billboard_albums_path = get_filename_billboard_data_all_years("csv")
    billboard_albums = pd.read_csv(
        billboard_albums_path, encoding="utf-8", sep=CSV_SEP, quotechar=CSV_QUOTE
    )
    billboard_albums["album"] = billboard_albums["album"].str.lower()
    grammy_billboard_merged = pd.merge(grammy_albums_of_the_year, billboard_albums, on="album")
    grammy_billboard_merged = grammy_billboard_merged.drop(columns=["artist_x", "link_img"])
    grammy_billboard_merged = grammy_billboard_merged.rename(
        columns={"artist_y": "artist", "year_y": "year"}
    )
    grammy_billboard_winners = grammy_billboard_merged.loc[grammy_billboard_merged["won"] == 1]
    # grammy_billboard_winners = grammy_billboard_winners.loc[grammy_billboard_winners["album"] == "come away with me"]
    # grammy_billboard_winners = grammy_billboard_winners.drop(
    #     grammy_billboard_winners[grammy_billboard_winners.year_x != grammy_billboard_winners.year].index)

    # ----------------------------------------------------------------------------------------
    # graph 3.2 - NOT READY
    billboard_albums_path = get_filename_billboard_data_all_years("csv")
    billboard_albums = pd.read_csv(
        billboard_albums_path, encoding="utf-8", sep=CSV_SEP, quotechar=CSV_QUOTE
    )
    billboard_albums["album"] = billboard_albums["album"].str.lower()

    metacritic_albums_path = get_filename_metacritic_data_all_years("csv")
    metacritic_albums = pd.read_csv(
        metacritic_albums_path, encoding="utf-8", sep=CSV_SEP, quotechar=CSV_QUOTE
    )
    metacritic_albums["year"] = pd.DatetimeIndex(metacritic_albums["release_date"]).year
    idx = (
        metacritic_albums.groupby(["year"])["metascore"].transform(max)
        == metacritic_albums["metascore"]
    )
    metacritic_best_review = metacritic_albums[idx]

    metacritic_best_review["album"] = metacritic_best_review["album"].str.lower()
    result_albums_bool = billboard_albums.album.isin(metacritic_best_review.album)
    result_albums = billboard_albums[result_albums_bool]

    # -------------------------------------------------------------------------------------------
    # graph 04
    grammy_indicated_artists = grammy_albums_of_the_year.groupby(["artist"]).count().reset_index()
    indication_df = grammy_indicated_artists["year"].value_counts()
    indication_df = indication_df.to_frame()
    # -------------------------------------------------------------------------------------------

    sns.set_theme(style="whitegrid")

    plt.figure()  # 1
    ax = sns.barplot(x="year", y="metascore", data=grammy_albums_mean_year)
    ax.set_title("Mean metascore for indicaded albums per year")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")

    plt.figure()  # 2
    bx = sns.barplot(x="year", y="metascore", data=grammy_albums_winners)
    bx.set_title("Metascore of winners albums per year")
    bx.set_xticklabels(bx.get_xticklabels(), rotation=40, ha="right")

    plt.figure()  # 3.1 - NOT READY
    bx = sns.scatterplot(x="year", y="rank", hue="album", data=grammy_billboard_winners)
    bx.set(xticks=grammy_billboard_winners.year.values)
    bx.tick_params(axis="x", rotation=40)
    bx.invert_yaxis()
    bx.legend_.remove()  # find a way to show name albums without plot over the graph
    # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    bx.set_title("Billboard rank of grammy winners per year")

    plt.figure()  # 3.2 - NOT READY
    bx = sns.scatterplot(x="year", y="rank", hue="album", data=result_albums)
    bx.set(xticks=result_albums.year.values)
    bx.tick_params(axis="x", rotation=40)
    bx.invert_yaxis()
    bx.legend_.remove()  # find a way to show name albums without plot over the graph
    # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    bx.set_title("Billboard rank of albums with best reviews on metacritic per year")

    plt.figure()  # 4
    cx = sns.barplot(x=indication_df.index, y="year", data=indication_df)
    cx.set_title("Artists quantity per number of indications")
    cx.set(xlabel="indications", ylabel="number of artists")

    plt.plot()
    plt.show()


if __name__ == "__main__":
    main()
