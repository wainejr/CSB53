import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
import random

cluster_filename = "../notebooks/albums_dist_to_clusters.csv"
all_data_filename = "../data/all_data.json"

def get_best_rank(df):

    df_billboard = df["billboard"]
    billboard_rank = []
    for v in df_billboard.values:
        best_value = 200
        if v is not None:
            for year, rank in dict(v).items():
                if rank < best_value:
                    best_value = rank
        billboard_rank.append(best_value)

    df['best_rank_billboard'] = billboard_rank
    return df


def do_linear_regression(logit_string, dataframe):
    model = smf.logit(logit_string, data=dataframe)
    response = model.fit()
    print(response.summary())
    print("\n")
    return response

def calculate_odds_ration(response):
    params = response.params
    conf = response.conf_int()
    conf['Odds Ratio'] = params
    conf.columns = ['5%', '95%', 'Odds Ratio']
    print(np.exp(conf))
    print("\n")

def main():
    # filename = "../data/all_data.json"
    df = pd.read_json(all_data_filename, convert_dates=["release_date"])
    # df = df[df["billboard"].notnull()]

    #region regular analysis
    df_vars = df[['metascore', 'grammy', 'billboard', 'release_date']]
    df_vars['release_date'] = df["release_date"].dt.month
    df_vars = df_vars.rename(columns={"release_date": "release_month"})
    df_log_reg = df_vars.copy()
    df_log_reg['grammy_indication'] = np.where((df_log_reg.grammy.isnull()), 0, 1)

    #df_log_reg['best_rank_billboard'] = np.where((df_log_reg.billboard.isnull()), 0, 1)
    df_log_reg = get_best_rank(df_log_reg)

    #normalising columns
    # df_log_reg['best_rank_billboard'] = (200 - df_log_reg['best_rank_billboard']) / 200
    # df_log_reg['metascore'] = df_log_reg['metascore'] / 100
    # df_log_reg['release_month'] = df_log_reg['release_month'] / 12
    #endregion


    #region models
    print("LOGISTIC REGRESSION WITH METASCORE \n")
    string = "grammy_indication ~ metascore"
    response = do_linear_regression(string, df_log_reg)
    calculate_odds_ration(response)

    print("LOGISTIC REGRESSION WITH BILLBOARD RANK \n")
    string = "grammy_indication ~ best_rank_billboard"
    response = do_linear_regression(string, df_log_reg)
    calculate_odds_ration(response)

    print("LOGISTIC REGRESSION WITH RELEASE MONTH \n")
    string = "grammy_indication ~ release_month"
    response = do_linear_regression(string, df_log_reg)
    calculate_odds_ration(response)

    print("LOGISTIC REGRESSION WITH ALL \n")
    string = "grammy_indication ~ metascore + best_rank_billboard + release_month"
    response_all = do_linear_regression(string, df_log_reg)
    calculate_odds_ration(response_all)

    #predict chance to be indicated
    for i in range(10):
        new_album = pd.DataFrame([{'metascore': random.randint(1, 100), 'best_rank_billboard': random.randint(1, 200),
                               'release_month': random.randint(1, 12)}])
        print(new_album)
        print("Chance to be indicated to grammy awards:")
        print(response_all.predict(new_album))
        print("\n")

    #endregion

    # region genres cluster
    df_genres = pd.read_csv(cluster_filename)

    df_complete_data = pd.merge(df, df_genres, on="link_album")
    df_selection = df_complete_data[[
        'metascore', 'grammy', 'billboard', 'release_date', 'Rap', 'Pop, RnB, Dance',
        'Mainstream Rock', 'Country', 'Rock Subgenres', 'Pop/Rock']]
    df_selection['release_date'] = df_selection["release_date"].dt.month
    df_selection = df_selection.rename(columns={"release_date": "release_month",
                                                "Pop, RnB, Dance": "Pop_RnB_Dance",
                                                "Mainstream Rock": "Mainstream_Rock",
                                                "Rock Subgenres": "Rock_Subgenres",
                                                "Pop/Rock": "Pop_Rock"})
    df_selection['grammy_indication'] = np.where((df_selection.grammy.isnull()), 0, 1)
    df_selection = get_best_rank(df_selection)

    print("LOGISTIC REGRESSION WITH GENRES \n")
    string = "grammy_indication ~ metascore + best_rank_billboard + release_month + Rap + Pop_RnB_Dance +" \
             " Mainstream_Rock + Country + Rock_Subgenres + Pop_Rock"
    response = do_linear_regression(string, df_selection)
    calculate_odds_ration(response)
    # endregion

    # region plots
    ax = sns.boxplot(y="best_rank_billboard", x="grammy_indication",
                     data=df_log_reg, color="cornflowerblue")
    ax.set_title("Billboard rank in relation to grammy indication")
    plt.gca().invert_yaxis()

    plt.plot()
    plt.show()

    bx = sns.boxplot(y="metascore", x="grammy_indication",
                     data=df_log_reg, color="cornflowerblue")
    bx.set_title("Metascore in relation to grammy indication")

    plt.plot()
    plt.show()
    # endregion

    #exit()

if __name__ == "__main__":
    main()
