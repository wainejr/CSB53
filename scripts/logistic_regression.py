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
    df_vars['release_date'] = df["release_date"].dt.month
    df_vars = df_vars.rename(columns={"release_date": "release_month"})
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
    # df_log_reg['best_rank_billboard'] = (200 - df_log_reg['best_rank_billboard']) / 200
    # df_log_reg['metascore'] = df_log_reg['metascore'] / 100
    # df_log_reg['release_month'] = df_log_reg['release_month'] / 12



    #region models
    model_1 = smf.logit("grammy_indication ~ metascore", data=df_log_reg)
    response1 = model_1.fit()
    print(response1.summary())

    params = response1.params
    conf = response1.conf_int()
    conf['Odds Ratio'] = params
    conf.columns = ['5%', '95%', 'Odds Ratio']
    print(np.exp(conf))

    model_2 = smf.logit("grammy_indication ~ best_rank_billboard", data=df_log_reg)
    response2 = model_2.fit()
    print(response2.summary())

    params = response2.params
    conf = response2.conf_int()
    conf['Odds Ratio'] = params
    conf.columns = ['5%', '95%', 'Odds Ratio']
    print(np.exp(conf))


    model_3 = smf.logit("grammy_indication ~ release_month", data=df_log_reg)
    response3 = model_3.fit()
    print(response3.summary())

    model_4 = smf.logit("grammy_indication ~ metascore + best_rank_billboard + release_month", data=df_log_reg)
    response4 = model_4.fit()
    print(response4.summary())

    params = response4.params
    conf = response4.conf_int()
    conf['Odds Ratio'] = params
    conf.columns = ['5%', '95%', 'Odds Ratio']
    print(np.exp(conf))

    new_album = pd.DataFrame([{'metascore': 80, 'best_rank_billboard': 200, 'release_month': 2004}])
    print("best_rank_billboard: 200")
    print(response2.predict(new_album))

    new_album = pd.DataFrame([{'metascore': 80, 'best_rank_billboard': 50, 'release_month': 2004}])
    print("best_rank_billboard: 50")
    print(response2.predict(new_album))

    new_album = pd.DataFrame([{'metascore': 80, 'best_rank_billboard': 1, 'release_month': 2004}])
    print("best_rank_billboard: 1")
    print(response2.predict(new_album))


    #endregion

    #region plots
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
    #endregion


#--------------------------------------------------------------------



    #exit()

if __name__ == "__main__":
    main()
