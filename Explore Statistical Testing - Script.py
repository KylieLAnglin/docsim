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


# In[58]:


similarity_pass(docs_transcripts, matrix_scripts, matrix_transcripts, 'study', '2017-18fall')


# In[33]:


(results['year'] + results['semester'] + results['scenario']).unique()


# ## Create distribution of within-study similarity

# This function will give us one single bootstrap. Holdout `holdout` documents, then compute the similarity within the same study for the remaining. If we do this lots of times, we'll get a distribution.

# In[26]:


def similarity_pass(df: pd.DataFrame, sim_matrix: pd.DataFrame, study_col: str = 'study',
                    study_val: str = '2017-18fall', holdout: float = 1/3, index_val: str = 'doc'):
    """Given a DataFrame and a value for column study, compute pairwise similarity metric 
        while holding out holdout proportion of values. This is a single pass."""
    
    df_copy = df.copy()
    sampled = df_copy[df_copy[study_col] == study_val].sample(frac=1 - holdout)
    indexed = sampled.set_index(index_val)
    
    matrix_copy = matrix.copy()
    matrix_indexed = matrix_copy.set_index(index_val)
    
    filtered_matrix = matrix_indexed[matrix_indexed.index.isin(indexed.index)]
    
    similarity = pairwise_distance(filtered_matrix, filtered_matrix)
    
    return np.mean(similarity)


# Try running it a few times.

# In[27]:


similarity_pass(df=df, sim_matrix=matrix, study_col='study', study_val='2017-18fall', holdout=0.4, index_val='doc')


# Now let's define a convenient lambda with our defaults.

# In[28]:


sim_pass = lambda study_val: similarity_pass(
    df=df, sim_matrix=matrix, study_col='study', study_val=study_val, holdout=0.4, index_val='doc'
)


# In[30]:


all_sims = []
for study_val in df['study'].unique():
    current_sims = [sim_pass(study_val) for _ in range(1000)]
    all_sims.append((study_val, current_sims))


# You could potentially speed this up using joblib.

# Save

# In[45]:


sims_dict = {k: v for (k, v) in all_sims}


# In[46]:


file = open(clean_filepath + 'within_sims_dict', 'wb')
pickle.dump(sims_dict, file)
file.close
file = open(clean_filepath + 'within_sims_dict', 'rb')
test = pickle.load(file)
file.close()


# Explore

# In[47]:


df['study'].unique()


# In[48]:


pd.Series(sims_dict['2017-18fall']).hist()


# In[49]:


pd.Series(sims_dict['2018-19fall']).hist()


# In[50]:


pd.Series(sims_dict['2017-18spring']).hist()


# In[54]:


pd.Series(sims_dict['2018-19spring']).hist()


# In[61]:


spring_sims_list = []
for i in sims_dict['2017-18spring']:
    spring_sims_list.append(i)
for i in sims_dict['2018-19spring']:
    spring_sims_list.append(i)
pd.Series(spring_sims_list).hist()


# In[52]:


all_sims_list = []
for i in all_sims:
    all_sims_list.extend(i[1])


# In[53]:


pd.Series(all_sims_list).hist()


# # Across-study distribution

# In[63]:


def across_similarity_pass(df: pd.DataFrame, sim_matrix: pd.DataFrame, study_col: str = 'study',
                    study_val1: str = '2017-18spring', study_val2: str = '2018-19spring', holdout: float = 1/3, index_val: str = 'doc'):
    """Given a DataFrame and a value for column study, compute pairwise similarity metric 
        while holding out holdout proportion of values. This is a single pass."""
    
    df_copy = df.copy()
    sampled1 = df_copy[df_copy[study_col] == study_val1].sample(frac=1 - holdout)
    sampled2 = df_copy[df_copy[study_col] == study_val2].sample(frac=1 - holdout)
    indexed1 = sampled1.set_index(index_val)
    indexed2 = sampled2.set_index(index_val)

    matrix_copy = matrix.copy()
    matrix_indexed = matrix_copy.set_index(index_val)
    
    filtered_matrix1 = matrix_indexed[matrix_indexed.index.isin(indexed1.index)]
    filtered_matrix2 = matrix_indexed[matrix_indexed.index.isin(indexed2.index)]
   
    similarity = pairwise_distance(filtered_matrix1, filtered_matrix2)
    
    return np.mean(similarity)


# Try running it a few times

# In[66]:


across_similarity_pass(df = df, sim_matrix = matrix, study_col = 'study',
                      study_val1 = '2017-18spring', study_val2 = '2018-19spring',
                      holdout = .4, index_val = 'doc')


# In[72]:


sim_pass = lambda study_val1, study_val2: across_similarity_pass(
    df=df, sim_matrix=matrix, study_col='study', 
    study_val1=study_val1, study_val2 = study_val2,
    holdout=0.4, index_val='doc'
)


# In[73]:


across_spring_sims = [sim_pass('2017-18spring', '2018-19spring') for _ in range(1000)]


# In[74]:


across_spring_sims


# In[83]:


bins = np.linspace(.2, .6, num = 40)
plt.title("Spring 2017-18 to Spring 2018-19")

plt.hist(spring_sims_list, bins,color = "green", label = "Within-Study Similarity", alpha = .2 )
plt.hist(across_spring_sims, bins,color = "blue", label = "Across-Study Similarity", alpha = .5 )

plt.legend()
plt.show()


# In[84]:


stats.ttest_ind(spring_sims_list, across_spring_sims)


# In[85]:


statistics.stdev(spring_sims_list)


# In[82]:


statistics.stdev(across_spring_sims)


# In[87]:


stats.kstest(spring_sims_list, 'norm')


# In[88]:


stats.kstest(across_spring_sims, 'norm')


# In[ ]:


# decrease holdout - what changes


# In[ ]:


sim_pass = lambda study_val: similarity_pass(
    df=df, sim_matrix=matrix, study_col='study', study_val=study_val, holdout=0.1, index_val='doc'
)

all_sims = []
for study_val in ['2017-18spring', '2018-19spring']:
    current_sims = [sim_pass(study_val) for _ in range(1000)]
    all_sims.append((study_val, current_sims))


# In[ ]:




