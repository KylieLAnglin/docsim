#!/usr/bin/env python
# coding: utf-8

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


# In[4]:


results = pd.read_csv(clean_filepath + 'results.csv')
results.sample(3)


# In[5]:


techniques = ['', '_stop', '_stop_wgt', '_stem_stop_wgt', '_lsa_wgt_stop']
columns = [2, 3, 4, 5, 6]


# In[6]:

# Script Similarity

file = table_filepath + 'table1_fidelity.xlsx'
wb = load_workbook(file)
ws = wb.active

row = 3
# Behavior
# Spring 2018
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2017-18') &
                           (results.semester == 'spring'))].script_sim.mean(),
                  2)
    ws.cell(row=row, column=col).value = value
wb.save(file)
row = row + 1

# Spring 2019
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2018-19') &
                           (results.semester == 'spring'))].script_sim.mean(),
                  2)
    ws.cell(row=row, column=col).value = value
wb.save(file)
row = row + 1

# Fall 2019
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2019-20') &
                           (results.semester == 'fall'))].script_sim.mean(),
                  2)
    ws.cell(row=row, column=col).value = value
wb.save(file)
row = row + 1

# Feedback
# Fall 2017
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2017-18') &
                           (results.semester == 'fall'))].script_sim.mean(),
                  2)
    ws.cell(row=row, column=col).value = value
wb.save(file)
row = row + 1

# Fall 2018
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2018-19') &
                           (results.semester == 'fall'))].script_sim.mean(), 2)
    ws.cell(row=row, column=col).value = value
wb.save(file)


# %% Study Similarity - Spring 2019 Baseline

file = table_filepath + 'table2_replicability.xlsx'
wb = load_workbook(file)
ws = wb.active

row = 3
# spring 2017
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2017-18') &
                           (results.semester == 'spring'))].study_sim_spring2017_18.mean(), 2)
    ws.cell(row=row, column=col).value = value
wb.save(file)
row = row + 1

# spring 2018
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2018-19') &
                           (results.semester == 'spring'))].study_sim_spring2017_18.mean(), 2)
    ws.cell(row=row, column=col).value = value
wb.save(file)
row = row + 1

# Spring 2018
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2019-20') &
                           (results.semester == 'fall'))].study_sim_spring2017_18.mean(), 2)
    ws.cell(row=5, column=col).value = value
wb.save(file)
row = row + 1

# Fall 2017
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2017-18') &
                           (results.semester == 'fall'))].study_sim_spring2017_18.mean(), 2)
    ws.cell(row=row, column=col).value = value
wb.save(file)
row = row + 1

# Fall 2018
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2018-19') &
                           (results.semester == 'fall'))].study_sim_spring2017_18.mean(), 2)
    ws.cell(row=row, column=col).value = value
wb.save(file)


# %% Study Matrix
file = table_filepath + 'table3_replicability_matrix.xlsx'
wb = load_workbook(file)
ws = wb.active


results = pd.read_csv(clean_filepath + 'results_lsa_wgt_stop.csv')

comps = ['study_sim_spring2017_18', 'study_sim_spring2018_19',
         'study_sim_fall2019_20',
         'study_sim_fall2017_18', 'study_sim_fall2018_19']
cols = [2, 3, 4, 5, 6]

row = 3
for comp, col in zip(comps, cols):
    value = round(results[((results.year == '2017-18') &
                           (results.semester == 'spring'))][comp].mean(), 2)
    ws.cell(row=row, column=col).value = value
wb.save(file)
row = row+1

for comp, col in zip(comps, cols):
    value = round(results[((results.year == '2018-19') &
                           (results.semester == 'spring'))][comp].mean(), 2)
    ws.cell(row=row, column=col).value = value
wb.save(file)
row = row+1

for comp, col in zip(comps, cols):
    value = round(results[((results.year == '2019-20') &
                           (results.semester == 'fall'))][comp].mean(), 2)
    ws.cell(row=row, column=col).value = value
wb.save(file)
row = row+1

for comp, col in zip(comps, cols):
    value = round(results[((results.year == '2017-18') &
                           (results.semester == 'fall'))][comp].mean(), 2)
    ws.cell(row=row, column=col).value = value
wb.save(file)
row = row+1

for comp, col in zip(comps, cols):
    value = round(results[((results.year == '2018-19') &
                           (results.semester == 'fall'))][comp].mean(), 2)
    ws.cell(row=row, column=col).value = value
wb.save(file)
row = row+1


# %%


sns.set()
sns.set_palette('husl', 8)

palette = sns.husl_palette(8)


def make_hist(title: str, value_list: list, color: str, range_list: list):

    bins = np.linspace(min(range_list), max(range_list), num=20)
    plt.title(title)

    plt.hist(value_list, bins, color=color, alpha=.5)


make_hist('Figure 1: Fidelity Scores - Behavior Study 1',
          results[(results.year == '2017-18') &
                  (results.semester == 'spring')].script_sim,
          'black', range_list=[0, .5])

make_hist('Figure 2: Fidelity Scores - Behavior Study 2',
          results[(results.year == '2018-19') &
                  (results.semester == 'spring')].script_sim,
          'gray', [0, .5])


plt.show()

# %%

results = pd.read_csv(clean_filepath + 'results_lsa_wgt_stop.csv')


bins = np.linspace(0, .5, num=30)
plt.title('Figure 1: Fidelity Scores for Behavior Study 1 and 2')

study1_values = results[(results.year == '2017-18') &
                        (results.semester == 'spring')].script_sim
plt.hist(study1_values, bins,
         color='darkgray', alpha=.75,
         label='Study 1')
sns.distplot(study1_values, hist=False, rug=False, color='darkgray')

study2_values = results[(results.year == '2018-19') &
                        (results.semester == 'spring')].script_sim
plt.hist(study2_values,
         bins, color='black', alpha=.5, label='Study 2')
sns.distplot(study2_values, hist=False, rug=False, color='black')


plt.legend(loc='upper right')
plt.xlabel("Fidelity Scores")
plt.ylabel("Number of Documents")
plt.savefig(table_filepath + 'Figure 1')

plt.show()
