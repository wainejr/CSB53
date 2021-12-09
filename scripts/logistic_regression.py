import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import MaxNLocator
import statsmodels.formula.api as smf




def main():
    filename = "../data/all_data.json"
    df = pd.read_json(filename, convert_dates=["release_date"])

    df_vars = df[['metascore', 'grammy', 'billboard', 'release_date']]
    df_vars['release_date'] = df["release_date"].dt.year
    df_log_reg = df_vars.copy()
    df_log_reg['grammy_indication'] = np.where((df_log_reg.grammy.isnull()), 0, 1)


    df_billboard = df_log_reg["billboard"]

    billboard_rank = []
    for v in df_billboard.values:
        best_value = 200
        if v is not None:
            for year, rank in dict(v).items():
                if rank < best_value:
                    best_value = rank
        billboard_rank.append(best_value)

    df_log_reg['best_rank_billboard'] = billboard_rank

    model_1 = smf.logit("grammy_indication ~ metascore", data=df_log_reg)
    response1 = model_1.fit()
    print(response1.summary())

    model_2 = smf.logit("grammy_indication ~ best_rank_billboard", data=df_log_reg)
    response2 = model_2.fit()
    print(response2.summary())

    model_3 = smf.logit("grammy_indication ~ release_date", data=df_log_reg)
    response3 = model_3.fit()
    print(response3.summary())

    model_4 = smf.logit("grammy_indication ~ metascore + best_rank_billboard + release_date", data=df_log_reg)
    response4 = model_4.fit()
    print(response4.summary())

    new_album = pd.DataFrame([{'metascore': 80, 'best_rank_billboard': 200, 'release_date': 2004}])
    print("best_rank_billboard: 200")
    print(response2.predict(new_album))

    new_album = pd.DataFrame([{'metascore': 80, 'best_rank_billboard': 50, 'release_date': 2004}])
    print("best_rank_billboard: 50")
    print(response2.predict(new_album))

    new_album = pd.DataFrame([{'metascore': 80, 'best_rank_billboard': 1, 'release_date': 2004}])
    print("best_rank_billboard: 1")
    print(response2.predict(new_album))
#--------------------------------------------------------------------



    exit()

    df_genres = df[['metascore', 'genres']]

    _df_genres = df_genres.set_index(['metascore'])['genres'].apply(pd.Series).stack().reset_index()
    _df_genres.columns = ['metascore', 'genre_num', 'genres']
    _df_genres_mean = _df_genres.groupby(["genres"]).mean().reset_index()

    _df_genres_most_frequently = _df_genres.groupby(['genres'])['metascore'].count().reset_index(name='Count')\
        .sort_values(['Count'], ascending=False).head(20)

    df21 = pd.merge(_df_genres, _df_genres_most_frequently, on=['genres'], how='left', indicator='Exist')
    df212 = df21[df21["Exist"] == "both"].sort_values(['Count'], ascending=False).reset_index()

    plt.figure()  # 1
    ax = sns.boxplot(x="genres", y="metascore", data=df212, color="cornflowerblue")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha="right")

    plt.plot()
    plt.show()

    df_billboard = df[df["billboard"].notnull()]
    _df_only_billboard = pd.DataFrame(df_billboard[["billboard", "metascore", "link_album"]])
    _all_billboard_data = {"metascore": [], "link_album": [], "rank": [], "year": []}
    for v in _df_only_billboard.values:
        for year, rank in dict(v[0]).items():
            _all_billboard_data["metascore"].append(v[1])
            _all_billboard_data["link_album"].append(v[2])
            _all_billboard_data["year"].append(int(year))
            _all_billboard_data["rank"].append(int(rank))

    _df_billboard = pd.DataFrame.from_dict(_all_billboard_data)
    _df_billboard = _df_billboard[["rank", "metascore"]]
    _df_rank_mean = _df_billboard.groupby(["rank"]).mean().reset_index()
    plt.figure()  # 1
    ax = sns.barplot(x="rank", y="metascore", data=_df_rank_mean)
    ax.set_title("Mean metascore for indicaded albums per year")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha="right")

    plt.plot()
    plt.show()
    #_df_billboard = _df_billboard.sort_values(by=['rank'])


    #- Metascore by position for Billboard (average)
    df_billboard = df[df["billboard"].notnull()]
    quebrando = df_billboard['billboard'].apply(pd.Series)
    df_billboard_concat = pd.concat([df_billboard["metascore"], df_billboard['billboard'].apply(pd.Series)], axis=1, join='outer')

    #
    df_genres = df[['metascore', 'genres']]
    _df_genres = df_genres.set_index(['metascore'])['genres'].apply(pd.Series).stack().reset_index()
    _df_genres.columns = ['metascore', 'genre_num', 'genre']
    _df_genres_mean = _df_genres.groupby(["genre"]).mean().reset_index()
    _df_genres_mean = _df_genres_mean[['metascore', 'genre']]

    plt.figure()  # 1
    ax = sns.boxplot(y=_df_genres_mean["metascore"])
    # ax = sns.barplot(x="year", y="metascore", data=grammy_albums_mean_year)
    # ax.set_title("Mean metascore for indicaded albums per year")
    # ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
    plt.plot()
    plt.show()

    #graph 01
    df_grammy = df[df["grammy"].notnull()]
    df_grammy = pd.concat([df_grammy, df_grammy['grammy'].apply(pd.Series)], axis=1, join='outer')

    grammy_albums_mean_year = df_grammy.groupby(["year"]).mean().reset_index()
    plt.figure()  # 1
    ax = sns.barplot(x="year", y="metascore", data=grammy_albums_mean_year)
    ax.set_title("Mean metascore for indicaded albums per year")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")

    plt.plot()
    plt.show()

    print(df)
    grammy_albums_of_the_year_path = get_filename_grammy_albums_of_the_year("csv")
    grammy_albums_of_the_year = pd.read_csv(
        grammy_albums_of_the_year_path, encoding="utf-8", sep=CSV_SEP, quotechar=CSV_QUOTE
    )
    grammy_albums_path = get_filename_metacritic_grammy_info("csv")
    grammy_albums = pd.read_csv(
        grammy_albums_path, encoding="utf-8", sep=CSV_SEP, quotechar=CSV_QUOTE
    )
    grammy_albums_merged = pd.merge(grammy_albums_of_the_year, grammy_albums, on="album")
    grammy_albums_merged = grammy_albums_merged.drop(columns=["artist_x"])
    grammy_albums_merged = grammy_albums_merged.rename(columns={"artist_y": "artist"})
    grammy_albums_mean_year = grammy_albums_merged.groupby(["year"]).mean().reset_index()

    plt.figure()  # 1
    ax = sns.barplot(x="year", y="metascore", data=grammy_albums_mean_year)
    ax.set_title("Mean metascore for indicaded albums per year")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")









    #------------------------------------------------
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
