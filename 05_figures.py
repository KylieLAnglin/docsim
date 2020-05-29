
# In[1]:


import pandas as pd
from openpyxl import load_workbook
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from library import start

# In[2]:

clean_filepath = start.clean_filepath
table_filepath = start.table_filepath

# In[3]:


docs = pd.read_csv(clean_filepath + 'text_transcripts.csv')
docs = docs.set_index('doc')
docs.sample(5)

# %%
results = pd.read_csv(clean_filepath + 'results_lsa_wgt_stop.csv')

# %% Figure 1
# Figure 1 

plt.figure(figsize=(10,10))
sns.set_style("white")


study1_values = results[(results.year == '2017-18') &
                        (results.semester == 'spring')].script_sim

study2_values = results[(results.year == '2018-19') &
                        (results.semester == 'spring')].script_sim

bins = np.linspace(0, .5, num=30)
plt.title('Figure 1: Fidelity Scores for Behavior Study 1 and 2')

plt.hist(study1_values, bins,
         color='darkgray', alpha=.75,
         label='Study 1')
sns.distplot(study1_values, hist=False, rug=False, color='darkgray')


plt.hist(study2_values,
         bins, color='black', alpha=.5, label='Study 2')
sns.distplot(study2_values, hist=False, rug=False, color='black')

plt.legend(loc='upper right')
plt.xlabel("Fidelity Scores")
plt.ylabel("Number of Documents")
plt.savefig(table_filepath + 'Figure 1')

plt.show()

# %% Explore by Coach

# Figure 2 Version 1
plt.figure(figsize=(10,10))
sns.set_style("white")

bins = np.linspace(0, .5, num=10)
plt.title('Figure 2: Fidelity Scores for Behavior Study 2 by Coach')

coach1 = results[(results.year == '2018-19') &
                 (results.semester == 'spring') &
                 (results.coach == 'Casedy')].script_sim
coach1_mean = round(coach1.mean(), 2)

coach2 = results[(results.year == '2018-19') &
                 (results.semester == 'spring') &
                 (results.coach == 'Emily')].script_sim
coach2_mean = round(coach2.mean(), 2)


coach3 = results[(results.year == '2018-19') &
                 (results.semester == 'spring') &
                 (results.coach == 'Bryan')].script_sim
coach3_mean = round(coach3.mean(), 2)


coach4 = results[(results.year == '2018-19') &
                 (results.semester == 'spring') &
                 (results.coach == 'Arielle')].script_sim
coach4_mean = round(coach4.mean(), 2)


sns.distplot(coach1, hist=False, rug=False, color='black',
             kde_kws={'linestyle': 'solid'}, label='Coach 1')

sns.distplot(coach2, hist=False, rug=False, color='black',
             kde_kws={'linestyle': 'dotted'}, label='Coach 2')

sns.distplot(coach3, hist=False, rug=False, color='black',
             kde_kws={'linestyle': 'dashed'}, label='Coach 3')

sns.distplot(coach4, hist=False, rug=False, color='black',
             kde_kws={'linestyle': 'dashdot'}, label='Coach 4')

plt.legend(loc='upper right')
plt.xlabel("Fidelity Scores")
plt.ylabel("Density")
plt.savefig(table_filepath + 'Figure 2 Fidelity Scores for Behavior Study 2 by Coach')

plt.show()

for coach in [coach1_mean, coach2_mean, coach3_mean, coach4_mean]:
    print(coach)

# %% Figure 2
# Figure 2 Version 2
plt.figure(figsize=(10, 10))
sns.set_style("white")

coach_code = {'Casedy': 1, 'Emily': 2, 'Bryan': 3, 'Arielle': 4}
results['coach_code'] = results['coach'].map(coach_code)


sns.boxplot(x='coach_code', y='script_sim', data=results[(results.year == '2018-19') &
                                                         (results.semester == 'spring')],
            color='white')
sns.swarmplot(x='coach_code', y='script_sim',
              data=results[(results.year == '2018-19') &
                           (results.semester == 'spring')],
              color="black")
plt.xlabel("Coach")
plt.ylabel("Fidelity Scores")
plt.savefig(table_filepath +
            'Figure 2b Fidelity Scores for Behavior Study 2 by Coach')

plt.show()
# %% Figure 3



plt.figure(figsize=(10,10))
sns.set_style("white")


study1_values = results[(results.year == '2017-18') &
                        (results.semester == 'spring')].script_sim
study2_values = results[(results.year == '2018-19') &
                        (results.semester == 'spring')].script_sim
study3_values = results[(results.year == '2019-20') &
                        (results.semester == 'fall')].script_sim
study4_values = results[(results.year == '2017-18') &
                        (results.semester == 'fall')].script_sim
study5_values = results[(results.year == '2018-19') &
                        (results.semester == 'fall')].script_sim

bins = np.linspace(0, .5, num=30)
plt.title('Figure 2: Fidelity Scores Across All Studies')


plt.hist(study1_values, bins,
         color='black', alpha=.75,
         label='Behavior Study 1')
# sns.distplot(study1_values, hist=False, rug=False, color='black')

plt.hist(study2_values, bins,
         color='gray', alpha=.75,
         label='Behavior Study 2')
# sns.distplot(study2_values, hist=False, rug=False, color='gray')

plt.hist(study3_values, bins,
         color='darkgray', alpha=.5,
         label='Behavior Study 3')
# sns.distplot(study3_values, hist=False, rug=False, color='darkgray')

plt.hist(study4_values, bins,
         color='silver', alpha=.5,
         label='Feedback Study 1')
# sns.distplot(study4_values, hist=False, rug=False, color='silver')

plt.hist(study5_values, bins,
         color='whitesmoke', alpha=.5,
         label='Feedback Study 2')
# sns.distplot(study5_values, hist=False, rug=False, color='whitesmoke')


plt.legend(loc='upper right')
plt.xlabel("Fidelity Scores")
plt.ylabel("Number of Documents")
plt.savefig(table_filepath + 'Figure 2b: Fidelity Scores Across All Studies')

plt.show()


# %%
