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
                           (results.semester == 'spring'))].script_sim.mean(), 2)
    ws.cell(row=row, column=col).value = value
wb.save(file)
row = row + 1

# Spring 2019
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2018-19') &
                           (results.semester == 'spring'))].script_sim.mean(), 2)
    ws.cell(row=row, column=col).value = value
wb.save(file)
row = row + 1

# Fall 2019
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2019-20') &
                           (results.semester == 'fall'))].script_sim.mean(), 2)
    ws.cell(row=row, column=col).value = value
wb.save(file)
row = row + 1

# Feedback
# Fall 2017
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2017-18') &
                           (results.semester == 'fall'))].script_sim.mean(), 2)
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


# In[8]:


# Session Similarity

file = table_filepath + 'Session Similarity.xlsx'
wb = load_workbook(file)
ws = wb.active

# Fall 2017
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2017-18') & (results.semester == 'fall'))].session_sim.mean(), 2)
    ws.cell(row= 3, column= col).value = value
wb.save(file)

# Fall 2018
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2018-19') & (results.semester == 'fall'))].session_sim.mean(), 2)
    ws.cell(row= 4, column= col).value = value
wb.save(file)

# Spring 2018
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2017-18') & (results.semester == 'spring'))].session_sim.mean(), 2)
    ws.cell(row= 5, column= col).value = value
wb.save(file)

# Spring 2019
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2018-19') & (results.semester == 'spring'))].session_sim.mean(), 2)
    ws.cell(row= 6, column= col).value = value
wb.save(file)

# Fall 2019
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2019-20') & (results.semester == 'fall'))].session_sim.mean(), 2)
    ws.cell(row= 7, column= col).value = value
wb.save(file)


# In[10]:


# Study Similarity - Spring 2019 Baseline

file = table_filepath + 'Study Similarity - Spring 2019 Baseline.xlsx'
wb = load_workbook(file)
ws = wb.active

# spring 2017
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2018-19') & (results.semester == 'spring'))].session_sim.mean(), 2)
    ws.cell(row= 3, column= col).value = value
wb.save(file)

# spring 2018
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2018-19') & (results.semester == 'spring'))].study_sim_spring2017_18.mean(), 2)
    ws.cell(row= 4, column= col).value = value
wb.save(file)

# Spring 2018
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2018-19') & (results.semester == 'spring'))].study_sim_fall2018_19.mean(), 2)
    ws.cell(row= 5, column= col).value = value
wb.save(file)


# In[14]:


# Study Similarity Matrix - Spring 2019 Baseline V2
file = table_filepath + 'Study Similarity - Spring 2019 Baseline V2.xlsx'
wb = load_workbook(file)
ws = wb.active

# fall 2017 
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2018-19') & (results.semester == 'spring'))].study_sim_fall2017_18.mean(), 2)
    ws.cell(row= 3, column= col).value = value
wb.save(file)

# fall 2018
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2018-19') & (results.semester == 'spring'))].study_sim_fall2018_19.mean(), 2)
    ws.cell(row= 4, column= col).value = value
wb.save(file)

# spring 2018
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2018-19') & (results.semester == 'spring'))].study_sim_spring2017_18.mean(), 2)
    ws.cell(row= 5, column= col).value = value
wb.save(file)

# spring 2019
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2018-19') & (results.semester == 'spring'))].study_sim_spring2018_19.mean(), 2)
    ws.cell(row= 6, column= col).value = value
wb.save(file)

# Fall 2019
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2018-19') & (results.semester == 'spring'))].study_sim_fall2019_20.mean(), 2)
    ws.cell(row= 7, column= col).value = value
wb.save(file)


# In[13]:


# Study Similarity Matrix - Fall 2019 Baseline V2
file = table_filepath + 'Study Similarity - Fall 2017 Baseline V2.xlsx'
wb = load_workbook(file)
ws = wb.active

# fall 2017 
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2017-18') & (results.semester == 'fall'))].study_sim_fall2017_18.mean(), 2)
    ws.cell(row= 3, column= col).value = value
wb.save(file)

# fall 2018
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2017-18') & (results.semester == 'fall'))].study_sim_fall2018_19.mean(), 2)
    ws.cell(row= 4, column= col).value = value
wb.save(file)

# spring 2018
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2017-18') & (results.semester == 'fall'))].study_sim_spring2017_18.mean(), 2)
    ws.cell(row= 5, column= col).value = value
wb.save(file)

# spring 2019
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2017-18') & (results.semester == 'fall'))].study_sim_spring2018_19.mean(), 2)
    ws.cell(row= 6, column= col).value = value
wb.save(file)

# Fall 2019
for tech, col in zip(techniques, columns):
    results = pd.read_csv(clean_filepath + 'results' + tech + '.csv')
    value = round(results[((results.year == '2017-18') & (results.semester == 'fall'))].study_sim_fall2019_20.mean(), 2)
    ws.cell(row= 7, column= col).value = value
wb.save(file)


# In[ ]:




