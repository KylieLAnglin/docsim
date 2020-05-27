
# # Session and Study Similarity
# * Session similarity for all five studies
# * Study Similarity
#     * Fall 2017 to Fall 2018 (Cross-Sample)
#     * Spring 2018 to Spring 2019 to Fall 2019 (Cross-Sample)
#     * Fall 2017 to Spring 2018 (Cross-Setting)
#     * Fall 2018 to Spring 2019 (Cross-Setting)
# * Each pre-processing technique receives its own df

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

docs = pd.read_csv(clean_filepath + 'text_transcripts.csv')
docs = docs.set_index('doc')
docs.sample(5)

def distance_to_mean(matrix_main, matrix_comparison):
    sims = []
    for maindoc in matrix_main.index:
        matrix_comp = matrix_comparison[~matrix_comparison.index.isin([maindoc])] # exclude self
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

def session_similarity(matrix_transcripts_file, text_df): 
    """
    Creates new variable for text_df containing session similarity.
    Returns new df with variable.
    """
    matrix_transcripts = pd.read_csv(clean_filepath + matrix_transcripts_file)
    matrix_transcripts = matrix_transcripts.set_index('doc')
    results = text_df[(text_df.year == '2017-18') & (text_df.semester == 'fall')]
    matrix = matrix_transcripts[matrix_transcripts.index.isin(results.index)]
    sims = distance_to_mean(matrix, matrix)
    results['session_sim'] = sims
    semesters = ['spring', 'fall', 'spring', 'fall']
    years = ['2017-18', '2018-19', '2018-19', '2019-20']
    for semester, year in zip(semesters, years):
        df = docs[(docs.year == year) & (docs.semester == semester)]
        matrix = matrix_transcripts[matrix_transcripts.index.isin(df.index)]
        sims = distance_to_mean(matrix, matrix)
        df['session_sim'] = sims
        results = results.append(df)
    return results

def study_similarity(matrix_transcripts_file, text_df):
    """
    Calculates the distance of every document to the mean of every study. 
    Returns new df with variable for every study distance.
    """
    semesters = ['fall', 'spring', 'fall', 'spring', 'fall']
    years = ['2017-18', '2017-18', '2018-19', '2018-19', '2019-20']

    matrix_transcripts = pd.read_csv(clean_filepath + matrix_transcripts_file)
    matrix_transcripts = matrix_transcripts.set_index('doc')

    for semester, year in zip(semesters, years):
        matrix = matrix_transcripts

        comp = text_df[(text_df.year == year) & (text_df.semester == semester)]
        matrix_comp = matrix_transcripts[matrix_transcripts.index.isin(comp.index)]

        sims = distance_to_mean(matrix, matrix_comp)
        results['study_sim_' + semester + year[0:4] + '_' + year[5:7]] = sims
    return results


def script_similarity(matrix_transcripts_file, matrix_scripts_file, text_df):
    
    # import matrices for transcripts and scripts
    matrix_transcripts = pd.read_csv(clean_filepath + matrix_transcripts_file)
    matrix_transcripts = matrix_transcripts.set_index('doc')

    matrix_scripts = pd.read_csv(clean_filepath + matrix_scripts_file)
    matrix_scripts = matrix_scripts.set_index('doc')

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

    # append feedback and behavior results
    script_results = feedback_results[['script_sim']]
    script_results = script_results.append(behavior_results[['script_sim']])
    
    return script_results

# No pre-processing
matrix_transcripts_file = 'matrix_transcripts.csv'
matrix_scripts_file = 'matrix_scripts.csv'
results = session_similarity(matrix_transcripts_file, docs) #creates session sim col
results = study_similarity(matrix_transcripts_file, docs)  # creates study sim cols

script_results = script_similarity(matrix_transcripts_file, matrix_scripts_file, docs)
results = results.merge(script_results, left_index = True, right_index = True)
results.to_csv((clean_filepath + 'results.csv'))

techniques = ['_stop', '_stop_wgt', '_stem', '_stem_stop', '_stem_stop_wgt', '_lsa', '_lsa_stop', '_lsa_wgt_stop']
for tech in techniques:
    matrix_transcripts_file = 'matrix_transcripts' + tech + '.csv'
    matrix_scripts_file = 'matrix_scripts' + tech + '.csv'
    results = session_similarity(matrix_transcripts_file, docs)
    results = study_similarity(matrix_transcripts_file, docs)
    script_results = script_similarity(matrix_transcripts_file, matrix_scripts_file, docs)
    results = results.merge(script_results, left_index = True, right_index = True)
    results.to_csv((clean_filepath + 'results' + tech + '.csv'))