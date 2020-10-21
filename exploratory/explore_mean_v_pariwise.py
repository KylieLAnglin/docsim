
# %%
import pandas as pd
from scipy import spatial
from openpyxl import load_workbook
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from library import start

clean_filepath = start.clean_filepath
table_filepath = start.table_filepath
# %%

transcript_df = pd.read_csv(clean_filepath + 'text_transcripts.csv')
transcript_df = transcript_df.set_index('doc')
transcript_df.sample(5)

# %%
script_df = pd.read_csv(clean_filepath + 'text_scripts.csv')
script_df = script_df.set_index('doc')
script_df.sample(5)

matrix_transcripts_file = 'matrix_transcripts_lsa_wgt_stop.csv'
matrix_scripts_file = 'matrix_scripts_lsa_wgt_stop.csv'

# %%

def distance_to_mean(matrix_main, matrix_comparison):
    sims = []
    for maindoc in matrix_main.index:
        matrix_comp = matrix_comparison[~matrix_comparison.index.isin(
            [maindoc])]  # exclude self
        centroid = np.mean(matrix_comp)
        sim = 1 - spatial.distance.cosine(matrix_main.loc[maindoc], centroid)
        sims.append(sim)
    return sims


def distance_to_doc(matrix_main, comp_doc):
    """
    Returns list of similarity of every doc in matrix_main to comp_doc
    """
    sims = []
    for maindoc in matrix_main.index:
        sim = 1 - spatial.distance.cosine(matrix_main.loc[maindoc], comp_doc)
        sims.append(sim)
    return sims

def pairwise_distance(matrix_main, matrix_comparison):
    ave_sims = []
    for maindoc in matrix_main.index:
        sims = []
        matrix_comp = matrix_comparison[~matrix_comparison.index.isin(
            [maindoc])]  # exclude self
        for compdoc in matrix_comp.index:
            sim = 1 - \
                spatial.distance.cosine(
                    matrix_main.loc[maindoc], matrix_comp.loc[compdoc])
            sims.append(sim)
        ave_sim = sum(sims)/len(sims)
        ave_sims.append(ave_sim)
    return ave_sims


# %%
def session_similarity_pair(matrix_transcripts_file, text_df):
    """
    Creates new variable for text_df containing session similarity.
    Returns new df with variable.
    """
    matrix_transcripts = pd.read_csv(clean_filepath + matrix_transcripts_file)
    matrix_transcripts = matrix_transcripts.set_index('doc')
    results = text_df[(text_df.year == '2017-18') &
                      (text_df.semester == 'fall')]
    matrix = matrix_transcripts[matrix_transcripts.index.isin(results.index)]
    sims = pairwise_distance(matrix, matrix)
    results['session_sim'] = sims
    semesters = ['spring', 'fall', 'spring', 'fall']
    years = ['2017-18', '2018-19', '2018-19', '2019-20']
    for semester, year in zip(semesters, years):
        df = text_df[(text_df.year == year) & (text_df.semester == semester)]
        matrix = matrix_transcripts[matrix_transcripts.index.isin(df.index)]
        sims = pairwise_distance(matrix, matrix)
        df['session_sim'] = sims
        results = results.append(df)
    return results

def session_similarity_mean(matrix_transcripts_file, text_df):
    """
    Creates new variable for text_df containing session similarity.
    Returns new df with variable.
    """
    matrix_transcripts = pd.read_csv(clean_filepath + matrix_transcripts_file)
    matrix_transcripts = matrix_transcripts.set_index('doc')
    results = text_df[(text_df.year == '2017-18') &
                      (text_df.semester == 'fall')]
    matrix = matrix_transcripts[matrix_transcripts.index.isin(results.index)]
    sims = distance_to_mean(matrix, matrix)
    results['session_sim'] = sims
    semesters = ['spring', 'fall', 'spring', 'fall']
    years = ['2017-18', '2018-19', '2018-19', '2019-20']
    for semester, year in zip(semesters, years):
        df = text_df[(text_df.year == year) & (text_df.semester == semester)]
        matrix = matrix_transcripts[matrix_transcripts.index.isin(df.index)]
        sims = distance_to_mean(matrix, matrix)
        df['session_sim'] = sims
        results = results.append(df)
    return results

# %%
results_pair = session_similarity_pair(matrix_transcripts_file, transcript_df)  

results_mean = session_similarity_mean(matrix_transcripts_file, transcript_df)

# %%
results_pair['feedback1'] = np.where((results_pair.scenario == 'feedback') & 
                                    (results_pair.semester == 'fall' )&
                                    (results_pair.year == '2017-18'), True, False)

results_pair['feedback2'] = np.where((results_pair.scenario == 'feedback') & 
                                    (results_pair.semester == 'fall' )&
                                    (results_pair.year == '2018-19'), True, False)

results_mean['feedback2'] = np.where((results_pair.scenario == 'feedback') & 
                                    (results_pair.semester == 'fall' )&
                                    (results_pair.year == '2018-19'), True, False)

results_mean['feedback1'] = np.where((results_pair.scenario == 'feedback') & 
                                    (results_pair.semester == 'fall' )&
                                    (results_pair.year == '2017-18'), True, False)

# %% Are pair and mean the same? 
results_pair[results_pair.feedback2 == True].session_sim.hist() 

results_mean[results_mean.feedback2 == True].session_sim.hist() 

# No but same distribution. Think about this later. 
                         