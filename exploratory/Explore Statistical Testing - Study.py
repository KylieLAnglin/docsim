#!/usr/bin/env python
# coding: utf-8

# In[80]:


import pandas as pd
from openpyxl import load_workbook
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import spatial, stats
import pickle
import statistics
from library import start


# In[42]:


clean_filepath = start.clean_filepath
table_filepath = start.table_filepath


# In[17]:


docs = pd.read_csv(clean_filepath + 'text_transcripts.csv')
docs = docs.set_index('doc')
docs.sample(5)


# In[18]:


matrix = pd.read_csv(clean_filepath + 'matrix_transcripts_lsa_wgt_stop.csv')
matrix


# In[19]:


results = pd.read_csv(clean_filepath + 'results_lsa_wgt_stop.csv')
results.sample(3)


# Goal: Create a distribution of similarities from one document to other documents _from its own study_.

# In[20]:


(results['year'] + results['semester']).unique()


# In[21]:


def add_study(df: pd.DataFrame) -> pd.DataFrame:
    """Add study column to an input DataFrame."""
    
    df_copy = df.copy()
    try:
        df_copy['study'] = df_copy['year'] + df_copy['semester']
    except KeyError:
        raise ValueError("DataFrame doesn't have the right columns.")
        
    return df_copy
        


# In[22]:


def pairwise_distance(matrix_main: pd.DataFrame, matrix_comparison: pd.DataFrame):
    """Given two document-term matrices, each indexed by document name, compute cosine similarity of every
        row in matrix_main to every row in matrix_comparison, unless they have the same index."""
    ave_sims = []
    for maindoc in matrix_main.index:
        sims = []
        matrix_comp = matrix_comparison[~matrix_comparison.index.isin([maindoc])] # exclude self
        for compdoc in matrix_comp.index:
            sim = 1 - spatial.distance.cosine(matrix_main.loc[maindoc], matrix_comp.loc[compdoc])
            sims.append(sim)
        ave_sim = sum(sims)/len(sims)
        ave_sims.append(ave_sim)
    return ave_sims


# In[23]:


df = add_study(results)


# In[24]:


df['study'].value_counts()


# In[25]:


matrix.head()


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




