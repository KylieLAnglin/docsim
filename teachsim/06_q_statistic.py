#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from scipy import spatial
from openpyxl import load_workbook
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
import numpy as np


# In[2]:


clean_filepath = "/Users/kylieleblancKylie/domino/docsim/data/clean/"
table_filepath = "/Users/kylieleblancKylie/domino/docsim/results/"


# In[3]:


docs = pd.read_csv(clean_filepath + 'text_corpus.csv')
docs = docs.set_index('doc')
docs.sample(5)


# In[5]:


matrix_corpus = pd.read_csv(clean_filepath + 'matrix_corpus.csv')
matrix_corpus = matrix_corpus.set_index('doc')
matrix_corpus.sample(5)


# In[6]:


def distance_to_mean(df, matrix_main, matrix_comparison):
    centroid = np.mean(matrix_comparison)
    sims = []
    for maindoc in matrix_main.index:
        sim = 1 - spatial.distance.cosine(matrix_main.loc[maindoc], centroid)
        sims.append(sim)
        #average = sum(pairwise_sim)/len(pairwise_sim)
        #df.at[maindoc, 'to_ideal'] = average
    
    return sims


# In[26]:


matrix_main = matrix_corpus[matrix_corpus.index.isin(list(docs[(docs.year == '2018-19') & (docs.semester == 'spring')].index))]
matrix_comparison = matrix_corpus[matrix_corpus.index.isin(list(docs[(docs.year == '2017-18') & (docs.semester == 'spring')].index))]
cross_setting = distance_to_mean(docs, matrix_main, matrix_comparison)


# In[27]:


matrix_main = matrix_corpus[matrix_corpus.index.isin(list(docs[(docs.year == '2018-19') & (docs.semester == 'spring')].index))]
matrix_comparison = matrix_corpus[matrix_corpus.index.isin(list(docs[(docs.year == '2018-19') & (docs.semester == 'fall')].index))]
cross_cohort = distance_to_mean(docs, matrix_main, matrix_comparison)


# In[9]:


matrix_main = matrix_corpus[matrix_corpus.index.isin(list(docs[(docs.year == '2018-19') & (docs.semester == 'spring')].index))]
matrix_comparison = matrix_corpus[matrix_corpus.index.isin(list(docs[(docs.year == '2018-19') & (docs.semester == 'spring')].index))]
cross_nothing = distance_to_mean(docs, matrix_main, matrix_comparison)


# In[29]:


cross_setting_mean = np.asarray(cross_setting).mean()
cross_setting_var = np.asarray(cross_setting).var()
cross_setting_weighted = (cross_setting_mean/cross_setting_var)
cross_setting_weight = 1/cross_setting_var
cross_setting_mean


# In[30]:


cross_cohort_mean = np.asarray(cross_cohort).mean()
cross_cohort_var = np.asarray(cross_cohort).var()
cross_cohort_weighted = (cross_cohort_mean/cross_cohort_var)
cross_cohort_weight = 1/cross_cohort_var
cross_cohort_mean


# In[10]:


cross_nothing_mean = np.asarray(cross_nothing).mean()
cross_nothing_var = np.asarray(cross_nothing).var()
cross_nothing_weighted = (cross_nothing_mean/cross_nothing_var)
cross_nothing_weight = 1/cross_nothing_var
cross_nothing_mean


# In[14]:


year = '2018-19'
semester = 'spring'
for maindoc in list(docs[(docs.year == year) & (docs.semester == semester)].index):
    pairwise_sim = []
    for doc in list(docs[(docs.year == year) & (docs.semester == semester)].index):
        sim = 1 - spatial.distance.cosine(matrix_corpus.loc[maindoc], matrix_corpus.loc[doc])
        pairwise_sim.append(sim)
    average = (sum(pairwise_sim) - 1)/(len(pairwise_sim) - 1) # don't include relationship with self
    average = (sum(pairwise_sim))/(len(pairwise_sim)) # don't include relationship with self
average


# In[32]:


tdot = (cross_setting_weighted + cross_cohort_weighted + cross_nothing_weighted)/(cross_setting_weight + cross_cohort_weight + cross_nothing_weight)
tdot


# In[33]:


cross_setting_q = (cross_setting_mean - tdot)**2/cross_setting_var
cross_cohort_q = (cross_cohort_mean - tdot)**2/cross_cohort_var
cross_nothing_q = (cross_nothing_mean - tdot)**2/cross_nothing_var


# In[34]:


q = cross_setting_q + cross_cohort_q + cross_nothing_q
q


# In[35]:


# physics rule
# less than 1.25 = negligible heterogeneity
q/(3-1)


# In[36]:


# k = number of studies
# personnel psychology
# l <= (k-1)/3
# medicine
# l <= 2(k-1)/2


# q = k - 1 + l <br/>
# q - l = k - 1 <br/>
# -l = k - 1 - q <br/>
# l = -1(k - 1- q) <br/>
# l = -k + 1 + q <br/>
# l = q + 1 - k <br/>

# In[37]:


l = q + 1 - 3
l


# In[ ]:




