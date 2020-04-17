#!/usr/bin/env python
# coding: utf-8

# In[48]:


import pandas as pd
from openpyxl import load_workbook
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import spatial, stats
import pickle
import statistics
import random
import typing
from library import start


# In[43]:


def distance_to_doc(matrix_main: pd.DataFrame, comp_doc: pd.DataFrame):
    """
    Returns list of similarity of every doc in matrix_main to comp_doc
    """
    sims = []
    for maindoc in matrix_main.index:
        sim = 1 - spatial.distance.cosine(matrix_main.loc[maindoc], comp_doc)
        sims.append(sim)    
    return sims


# In[44]:


def feedback_sim(matrix_transcripts: pd.DataFrame, matrix_scripts: pd.DataFrame, text_df:pd.DataFrame):
    """ Takes a doc-term matrix of transcripts and scripts and a text dataframe.
    Caluclates similarity of every feedback doc in transcripts to every feedback script.
    Create column for each. 
    Then creates column of max.
    """
    
    # limit to feedback scripts
    feedback_results = text_df[(text_df.scenario == 'feedback')]
    feedback_matrix = matrix_transcripts[matrix_transcripts.index.isin(feedback_results.index)]
    feedback_scripts = matrix_scripts[matrix_scripts.index.str.contains('Feedback')]

    # sim to feedback script
    script_indices = []
    script_names = []
    for doc in feedback_scripts.index: #save list of script names that are just letter and number
        script_indices.append(str(doc))
        script_names.append(str(doc[15:18]))

    for script, col in zip(script_indices, script_names):
        sims = distance_to_doc(feedback_matrix, feedback_scripts.loc[script])
        feedback_results[col] = sims
        
    # keep max value
    feedback_results['script_sim'] = feedback_results[script_names].max(axis=1)
    
    return feedback_results[['script_sim']]


# In[45]:


def behavior_sim(matrix_transcripts_file: str, matrix_scripts_file: str, text_df: pd.DataFrame):
    # limit to behavior transciprs
    behavior_results = text_df[(text_df.scenario == 'behavior')]
    behavior_matrix = matrix_transcripts[matrix_transcripts.index.isin(behavior_results.index)]
    behavior_scripts = matrix_scripts[matrix_scripts.index.str.contains('Classroom Management')]

    # sim to behavior transcript
    script_indices = []
    script_names = []
    for doc in behavior_scripts.index:
        script_indices.append(str(doc))
        script_names.append(str(doc[27:29]))

    for script, col in zip(script_indices, script_names):
        sims = distance_to_doc(behavior_matrix, behavior_scripts.loc[script])
        behavior_results[col] = sims
    
    # keep max value
    behavior_results['script_sim'] = behavior_results[script_names].max(axis=1)
    
    return behavior_results[['script_sim']]


# In[46]:


clean_filepath = start.clean_filepath
table_filepath = start.table_filepath

docs_transcripts = pd.read_csv(clean_filepath + 'text_transcripts.csv')
docs_transcripts = docs_transcripts.set_index('doc')

docs_scripts = pd.read_csv(clean_filepath + 'text_scripts.csv')
docs_scripts = docs_scripts.set_index('doc')

matrix_transcripts = pd.read_csv(clean_filepath + 'matrix_transcripts_lsa_wgt_stop.csv')
matrix_transcripts = matrix_transcripts.set_index('doc')

    
matrix_scripts = pd.read_csv(clean_filepath + 'matrix_scripts_lsa_wgt_stop.csv')
matrix_scripts = matrix_scripts.set_index('doc')


results = pd.read_csv(clean_filepath + 'results_lsa_wgt_stop.csv')


# In[31]:


feedback_results = feedback_sim(matrix_transcripts, matrix_scripts, text_df = docs_transcripts)

# Goal: Create a distribution of similarities from documents to the ideal script

# Start with feedback

# In[53]:


def add_study(df: pd.DataFrame) -> pd.DataFrame:
    """Add study column to an input DataFrame."""
    
    df_copy = df.copy()
    try:
        df_copy['study'] = df_copy['year'] + df_copy['semester']
    except KeyError:
        raise ValueError("DataFrame doesn't have the right columns.")
        
    return df_copy


# In[54]:


docs_transcripts = add_study(docs_transcripts)


# In[57]:
# This function will give us one single bootstrap. Holdout `holdout` documents, then compute the similarity within the same study for the remaining. If we do this lots of times, we'll get a distribution.

def similarity_pass(df: pd.DataFrame, script_matrix: pd.DataFrame, sim_matrix: pd.DataFrame,
                    study_col: str = 'study',
                    study_val: str = '2017-18fall', 
                    scenario_func: typing.Callable = feedback_sim):
    """Given a DataFrame and a value for column study, compute pairwise similarity metric 
        while holding out holdout proportion of values. This is a single pass."""
    df_copy = df.copy()
    filtered_df = df_copy[df_copy[study_col] == study_val]
    sampled_indices = random.choices(filtered_df.index, k = len(filtered_df))
    
    matrix_copy = sim_matrix.copy()
    
    filtered_matrix = matrix_copy[matrix_copy.index.isin(sampled_indices)]
    similarity = scenario_func(filtered_matrix, script_matrix, df_copy[df_copy.index.isin(sampled_indices)])
    return similarity.mean()



# In[33]:

study_func_dict = {'2017-18fall': feedback_sim,
'2017-18spring': behavior_sim,
'2018-19fall': feedback_sim,
'2018-19spring': behavior_sim,
'2019-20fall': behavior_sim}

# try running it a few times
for study_val in study_func_dict:
    similarity_pass(df = docs_transcripts, script_matrix = matrix_scripts, 
    sim_matrix = matrix_transcripts, study_col = 'study', study_val = study_val,
    scenario_func = study_func_dict[study_val])

# Now let's define a convenient lambda with our defaults.

sim_pass = lambda study_val, scenario_func: similarity_pass(
    df=docs_transcripts, script_matrix = matrix_scripts, sim_matrix=matrix_transcripts,
    study_col='study', study_val=study_val, scenario_func=scenario_func
)


# In[30]:



all_sims = []
for study_val in study_func_dict:
    current_sims = [sim_pass(study_val, study_func_dict[study_val]) for _ in range(1000)]
    all_sims.append((study_val, current_sims))


# You could potentially speed this up using joblib.

# Save

# In[45]:


sims_dict = {k: v for (k, v) in all_sims}


# In[46]:


file = open(clean_filepath + 'script_sims_dict', 'wb')
pickle.dump(sims_dict, file)
file.close
file = open(clean_filepath + 'script_sims_dict', 'rb')
test = pickle.load(file)
file.close()
