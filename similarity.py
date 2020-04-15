
# coding: utf-8

# In[151]:


import docx
import os
import nltk
import re
from nltk import sent_tokenize, word_tokenize

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


def dict_doc_similarity(doc_list, sim_list):
    sim_dict = {}
    for key, value in zip(doc_list, sim_list):
        sim_dict[key] = value

    return sim_dict


def calc_within_group_sim_metrics(filepath, pattern, alt_coach_titles = True):
    """
    All documents within the filepath need to be docx files
    alt_coach_titles is a dictionary with the filename and coach synonym
    :param filepath:
    :return:
    """
    doc_text = make_text_dict(filepath, pattern)
    corpus = list(doc_text.values())
    vectorizer = CountVectorizer()  # automatically tokenizes all words >2 characteris
    vectors = vectorizer.fit_transform(corpus)
    corpus_array = vectors.toarray()
    centroid = corpus_array.mean(axis=0)

    sim_to_centroid = []
    for doc in corpus_array:
        sim_to_centroid.append(1 - spatial.distance.cosine(doc, centroid))

    sim_centroid_mean = statistics.mean(sim_to_centroid)
    sim_centroid_sd = statistics.stdev(sim_to_centroid)
    print("Average similarity to centroid: % 5.2f" % (sim_centroid_mean))
    print("Standard deviation of similarity to centroid: % 5.2f" % (sim_centroid_sd))

    sim_pairwise_matrix = metrics.pairwise.cosine_similarity(vectors, dense_output=True)
    sim_pairwise = sim_pairwise_matrix.mean(axis=1)
    sim_pairwise = list(sim_pairwise)


    sim_pairwise_mean = statistics.mean(sim_pairwise)
    sim_pairwise_sd = statistics.stdev(sim_pairwise)
    print("Average pairwise similarity: % 5.2f" % (sim_pairwise_mean))
    print("Standard deviation of pairwise similarity: % 5.2f" % (sim_pairwise_sd))

    return doc_text, sim_to_centroid, sim_pairwise


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
                fullText.append(new_text)
    return '\n'.join(fullText)


def replace_alt_words_for_coach(string):
    new_text = string.replace('Instructor:  [', 'Coach:  [')
    new_text = new_text.replace('Tutor:  [', 'Coach:  [')
    new_text = new_text.replace('Interviewer:  [', 'Coach:  [')
    new_text = new_text.replace('Interviewer: [', 'Coach:  [')
    new_text = new_text.replace('COACH: [', 'Coach:  [')
    new_text = new_text.replace('Interviewer:', 'Coach:')

    return new_text
replace_alt_words_for_coach('Instructor:  [00:00:00] All right.  So what do you think of that? How did this simulation go? [00:00:05]')






