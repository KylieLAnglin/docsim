# %%
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import statistics
import numpy as np
from library import start

sns.set()
sns.set_palette('husl', 8)

palette = sns.husl_palette(8)

# %%
file = open(start.clean_filepath + 'script_sims_dict', 'rb')
script_sims_dict = pickle.load(file)

results = pd.read_csv(start.clean_filepath + 'results_lsa_wgt_stop.csv')


def make_list_from_dict_tuples(sim_dict: dict, dict_key: str):
    sim_list = []
    for value in sim_dict[dict_key]:
        sim_list.append(value[0])
    return sim_list


def make_hist(title: str, boot_list: list, color_int: int):

    bins = np.linspace(min(boot_list), max(boot_list), num=50)
    plt.title(title)

    plt.hist(boot_list, bins, color=palette[color_int])

    plt.show()


# %% 2017-18fall
fall1718_boots = make_list_from_dict_tuples(sim_dict=script_sims_dict,
                                            dict_key='2017-18fall')

make_hist(title="Script Similarity - Fall 2017-18 " \
          "Feedback Bootstrapped Distribution",
          boot_list=fall1718_boots, color_int=3)

fall1718_results = list(results[(results.year == '2017-18') &
                                (results.semester == 'fall')].script_sim)

make_hist(title="Script Similarity - Fall 2017-18 Feedback",
          boot_list=fall1718_results, color_int=0)


# %% 2017-18 Spring
spring1718_boots = make_list_from_dict_tuples(sim_dict=script_sims_dict,
                                              dict_key='2017-18spring')

make_hist(title="Script Similarity - Spring 2017-18 Behavior",
          boot_list=spring1718_boots)


# %% 2018-19 Fall
fall1819_boots = make_list_from_dict_tuples(sim_dict=script_sims_dict,
                                            dict_key='2018-19fall')

make_hist(title="Script Similarity - Fall 2018-19 Feedback",
          boot_list=fall1819_boots, color_int=3)


# %%
spring1819_boots = make_list_from_dict_tuples(sim_dict=script_sims_dict,
                                              dict_key='2018-19spring')

make_hist(title="Script Similarity - Spring 2018-19 Behavior",
          boot_list=spring1819_boots, color_int=4)

# %%
fall1920_boots = make_list_from_dict_tuples(sim_dict=script_sims_dict,
                                            dict_key='2019-20fall')

make_hist(title="Script Similarity - Fall 2019-20 Behavior",
          boot_list=fall1920_boots, color_int=5)

# %%
