
# coding: utf-8

# # Import and Clean Scripts

# In[1]:


import docx
import os
import nltk
import re
from nltk import sent_tokenize, word_tokenize
import pandas as pd

from nltk import WordNetLemmatizer 
import operator

import fnmatch

import statistics
lemmatizer = WordNetLemmatizer() 

from sklearn.feature_extraction.text import TfidfVectorizer

from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy import spatial
from sklearn import metrics


# In[2]:


ideal_filepath = '/Users/kylieleblancKylie/domino/docsim/data/models/'
clean_filepath = "/Users/kylieleblancKylie/domino/docsim/data/clean/"


# # Extract Text from Documents

# In[3]:


def make_text_dict(filepath, pattern):
    os.chdir(filepath)
    doc_text = {}
    for file in os.listdir():
        if fnmatch.fnmatch(file, pattern):
            doc_text[file] = clean_text(filepath + file)
    return doc_text

def clean_text(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        new_text = para.text
        new_text = fix_typos(new_text)
        fullText.append(new_text)
    new_text = ' '.join(fullText)
    return new_text

def fix_typos(string):
    new_text = string.replace('00:00:11]', '')
    new_text = new_text.replace('Dave', 'Dev')
    return new_text


# In[4]:


ideal_behavior_dict = make_text_dict(ideal_filepath, 'Classroom Management Model*')
ideal_behavior_dict


# In[5]:


ideal_feedback_dict = make_text_dict(ideal_filepath, 'Feedback Model*')


# In[6]:


def create_df(textdict, scenario):
    df = pd.DataFrame.from_dict(data = textdict, orient = 'index').reset_index()
    df = df.rename({'index': 'doc', 0: 'text'}, axis = 'columns')
    df['scenario'] = scenario
    df = df.set_index('doc')
    return df
ideal_feedback = create_df(ideal_feedback_dict, 'feedback')
ideal_behavior = create_df(ideal_behavior_dict,'behavior')


# In[7]:


ideal_corpus_df = ideal_feedback.append(ideal_behavior)
ideal_corpus_df.sample(5)


# # Send to CSV

# In[8]:


ideal_corpus_df.to_csv(clean_filepath + 'text_scripts.csv')

