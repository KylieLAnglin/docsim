
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

sns.set_style("white")

# %% Fidelity Results
###
# Fidelity Results
###
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

# %% Figure 1 Fidelity Score Distributions

fig = plt.figure(figsize=(10, 10))
ax = plt.axes()

ax.set_title('Figure 1: Fidelity Score Distributions', fontsize=15)

bins = np.linspace(0, .5, num=10)

sns.distplot(study1_values, hist=False, rug=False, color='0.01',
             kde_kws={'linestyle': 'solid'}, label='Behavior Study 1')

sns.distplot(study2_values, hist=False, rug=False, color='black',
             kde_kws={'linestyle': 'dashed'}, label='Behavior Study 2')

sns.distplot(study3_values, hist=False, rug=False, color='black',
             kde_kws={'linestyle': 'dotted'}, label='Behavior Study 3')

sns.distplot(study4_values, hist=False, rug=False, color='lightgray',
             kde_kws={'linestyle': 'solid'}, label='Feedback Study 1')

sns.distplot(study5_values, hist=False, rug=False, color='lightgray',
             kde_kws={'linestyle': 'dashed'}, label='Feedback Study 2')

ax.legend(loc='upper right')
ax.set_xlabel("Fidelity Scores")
ax.set_ylabel("Kernel Density")
notes = "Notes: Fidelity scores are estimated by calculating the " \
    "similarity between each transcript and an ideal script. " \
    "A higher score indicates higher fidelity to the script."
fig.text(.1, .05, notes, ha='left', wrap=True)

fig.savefig(table_filepath + 'Figure 1 Fidelity Score Distributions',
            bbox='tight', pad_inches=0.05)


for study in [study1_values, study2_values, study3_values,
              study4_values, study5_values]:
    print(study.std())

# %% Figure 2
fig = plt.figure(figsize=(10, 10))
ax = plt.axes()

ax.set_title('Figure 2: Fidelity Scores for Feedback Study 2 by Coach',
             fontsize=15)

coach_code = {'Casedy': 'C', 'Sarah': 'A', 'Alex': 'D', 'Arielle': 'B'}
results['coach_code'] = results['coach'].map(coach_code)


sns.boxplot(x='coach_code', y='script_sim',
            data=results[(results.year == '2018-19') &
                         (results.semester == 'fall')],
            color='white')
sns.swarmplot(x='coach_code', y='script_sim',
              data=results[(results.year == '2018-19') &
                           (results.semester == 'fall')],
              color="black")

ax.set_xlabel("Coach")
ax.set_ylabel("Fidelity Scores")

notes = "Notes: Fidelity scores are estimated by calculating" \
    " the similarity between" \
    " each transcript and an ideal script. " \
    "A higher score indicates \n " \
    "higher fidelity to the script." \
    "Boxes indicate the 50th percentile and interquartile range. " \
    "Whiskers extend to all scores within 1.5 \n times the" \
    " interquartile range. "
fig.text(.1, .025, notes, ha='left', wrap=True)


fig.savefig(table_filepath +
            'Figure 2 Fidelity Scores for Feedback Study 2 by Coach')
plt.show()

for coach in ['A', 'B', 'C', 'D']:
    print(results[(results.semester == 'fall') &
                  (results.year == '2018-19') &
                  (results.coach_code == coach)].script_sim.median())

# %% Figure 3: Panel of Histograms


fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(10, 10))
ax1 = axs[0, 0]
ax2 = axs[0, 1]
ax3 = axs[0, 2]
ax4 = axs[1, 0]
ax5 = axs[1, 1]

bins = np.linspace(0, .75, num=30)

fig.suptitle('Figure 3: Fidelity Scores  with Unusual Transcripts Highlighted',
             fontsize=15)

ax1.hist(study1_values, bins,
         color='darkgray', alpha=.75)
ax1.set_xlabel('Behavior Study 1')

ax2.hist(study2_values, bins,
         color='darkgray', alpha=.75)
ax2.set_xlabel('Behavior Study 2')
ax2.hist(study2_values.where(study2_values < .2), bins,
         color='black')

ax3.hist(study3_values, bins,
         color='darkgray', alpha=.75)
ax3.set_xlabel('Behavior Study 3')
ax3.hist(study3_values.where(study3_values > 0.36), bins,
         color='black')

ax4.hist(study4_values, bins,
         color='darkgray', alpha=1)
ax4.set_xlabel('Feedback Study 1')
ax4.hist(study4_values.where((study4_values < .09) | (study4_values > 0.31)),
         bins, color='black')

ax5.hist(study5_values, bins,
         color='darkgray', alpha=1)
ax5.set_xlabel('Feedback Study 2')
ax5.hist(study5_values.where((study5_values > 0.61)), bins,
         color='black')

for ax in [ax1, ax2, ax3, ax4, ax5]:
    ax.set_ylim(0, 20)

fig.delaxes(axs[1, 2])

notes = "Notes: Fidelity scores are estimated by calculating the " \
    "similarity between each transcript and an ideal script. " \
    "A higher score  \nindicates higher fidelity to the script. " \
    "Potentially abnormal transcripts (based on visual examination) " \
    "are highlighted in black. \nThese are the transcripts we have" \
    " flagged for manual observation."
fig.text(.1, .025, notes, ha='left')

plt.savefig(table_filepath + 'Figure 3: Fidelity Panels', dpi=200)


# %% Figure 2b
# Figure 2 Version 2
plt.figure(figsize=(10, 10))
sns.set_style("white")

coach_code = {'Casedy': 1, 'Emily': 2, 'Bryan': 3, 'Arielle': 4}
results['coach_code'] = results['coach'].map(coach_code)


sns.boxplot(x='coach_code', y='script_sim',
            data=results[(results.year == '2018-19') &
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
