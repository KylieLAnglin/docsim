
# coding: utf-8

# # Clean Text
# * Import Transcripts
# * Extract Coach Text
# * Remove Time Labels
# * Replace avatar names for key words?
# * Create transcript dataframe

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


fall2017_filepath = '/Users/kylieleblancKylie/domino/docsim/data/fall_2017/coaching/'
fall2018_filepath = '/Users/kylieleblancKylie/domino/docsim/data/fall_2018/coaching/'
spring2018_filepath = '/Users/kylieleblancKylie/domino/docsim/data/spring_2018/coaching/'
spring2019_filepath = '/Users/kylieleblancKylie/domino/docsim/data/spring_2019/coaching/'
fall2019_filepath = "/Users/kylieleblancKylie/domino/docsim/data/fall_2019_TAP/coaching/"

clean_filepath = "/Users/kylieleblancKylie/domino/docsim/data/clean/"




# In[3]:


def make_text_dict(filepath, pattern):
    os.chdir(filepath)
    doc_text = {}
    for file in os.listdir():
        if fnmatch.fnmatch(file, pattern):
            doc_text[file] = getCoachText(filepath + file)
    return doc_text

def getCoachText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        if len(para.text) > 5:
            new_text = replace_alt_words_for_coach(para.text)
            if new_text[0:6] == 'Coach:' or new_text[11:17] == 'Coach:':
                new_text = drop_labels(new_text)
                new_text = fix_typos(new_text)
                fullText.append(new_text)
    new_text = ' '.join(fullText)
    #new_text = new_text.replace('\\n','')
    return new_text

def replace_alt_words_for_coach(string):
    new_text = string.replace('Instructor:', 'Coach:')
    new_text = new_text.replace('Tutor:', 'Coach:')
    new_text = new_text.replace('Interviewer:', 'Coach:')
    new_text = new_text.replace('Interviewer:', 'Coach:')
    new_text = new_text.replace('COACH:', 'Coach:')
    new_text = new_text.replace('Interviewer:', 'Coach:')
    new_text = new_text.replace('Announcer:', 'Coach:')
    new_text = new_text.replace('Female Speaker:', 'Coach:')
    new_text = new_text.replace('Male Speaker:', 'Coach:')
    new_text = new_text.replace('Arielle:', 'Coach:')
    new_text = new_text.replace('Mike Grille:', 'Coach:')
    new_text = new_text.replace('Rosalie:', 'Coach:')
    new_text = new_text.replace('Moderator:', 'Coach:')
    new_text = new_text.replace('Anna Myers:', 'Coach:')
    return new_text

def drop_labels(string):
    new_text = string.replace('\\n','')
    new_text = re.sub(r'\[(.*?)\]', '', new_text)
    new_text = re.sub(r'([a-zA-Z]+)\:', '', new_text)
    return new_text

def fix_typos(string):
    new_text = string.replace('00:00:11]', '')
    new_text = new_text.replace('Dave', 'Dev')
    return new_text

def create_df(textdict, year, semester, scenario):
    df = pd.DataFrame.from_dict(data = textdict, orient = 'index').reset_index()
    df = df.rename({'index': 'doc', 0: 'text'}, axis = 'columns')
    df['year'] = year
    df['semester'] = semester
    df['scenario'] = scenario
    df = df.set_index('doc')
    return df

# In[4]:


fall2017_dict = make_text_dict(fall2017_filepath, '*Transcript*')
spring2018_dict = make_text_dict(spring2018_filepath, '*docx')
fall2018_dict = make_text_dict(fall2018_filepath, '2018*docx')
spring2019_dict = make_text_dict(spring2019_filepath, '2019*')
fall2019_dict = make_text_dict(fall2019_filepath, '*Transcript.docx')


# In[5]:


fall2019_dict['01_1920_05_031_22c_Transcript.docx']


# In[6]:


fall2018_dict['2018_112_3C_Transcript.docx']


# ## Create dataframe

# In[7]:



fall2017 = create_df(fall2017_dict, '2017-18', 'fall', 'feedback')
spring2018 = create_df(spring2018_dict, '2017-18', 'spring', 'behavior')
fall2018 = create_df(fall2018_dict, '2018-19', 'fall', 'feedback')
spring2019 = create_df(spring2019_dict, '2018-19', 'spring', 'behavior')
fall2019 = create_df(fall2019_dict, '2019-20', 'fall', 'behavior')


# In[8]:


spring2019.sample()


# In[9]:


corpus_df = fall2017.append(spring2018)
corpus_df = corpus_df.append(fall2018)
corpus_df = corpus_df.append(spring2019)
corpus_df = corpus_df.append(fall2019)
corpus_df.sample(10)


# # Send to CSV

# In[10]:


corpus_df.to_csv(clean_filepath + 'text_transcripts.csv')

