# %%
import pandas as pd
from library import start

clean_filepath = start.clean_filepath
table_filepath = start.table_filepath

# %%
# %%

transcript_df = pd.read_csv(clean_filepath + 'text_transcripts.csv')
transcript_df = transcript_df.set_index('doc')
transcript_df.sample(5)

# %%
script_df = pd.read_csv(clean_filepath + 'text_scripts.csv')
script_df = script_df.set_index('doc')
script_df.sample(5)

# %%
def import_limited_matrices(matrix_file: str,
                            limited_text_df: pd.DataFrame):
    matrix = pd.read_csv(clean_filepath + matrix_file)
    matrix = matrix.set_index('doc')

    # limit to scenario scripts
    limited_matrix = matrix[matrix.index.isin(
        limited_text_df.index)]

    return limited_matrix

# %%


scenario = 'feedback'
semester= 'fall'
year = '2018-19'

limited_df = transcript_df[(transcript_df.scenario == scenario) & 
                (transcript_df.semester == semester) & 
                (transcript_df.year == year)]

transcripts = import_limited_matrices('matrix_transcripts.csv', limited_df)
scripts = import_limited_matrices('matrix_scripts.csv', script_df[(
    script_df.scenario == scenario)])

transcripts_mean = transcripts.agg(['mean'])
transcripts_mean = transcripts_mean.sort_values(by = 'mean', axis = 1,
ascending = False)
transcripts_mean

# %%
scripts = import_limited_matrices('matrix_scripts.csv', script_df[(
    script_df.scenario == scenario)])

scripts_mean = scripts.agg(['mean'])
scripts_mean = scripts_mean.sort_values(by = 'mean', axis = 1,
ascending = False)
scripts_mean

# %%

scenario = 'behavior'
semester= 'spring'
year = '2018-19'

limited_df = transcript_df[(transcript_df.scenario == scenario) & 
                (transcript_df.semester == semester) & 
                (transcript_df.year == year)]

transcripts = import_limited_matrices('matrix_transcripts.csv', limited_df)
scripts = import_limited_matrices('matrix_scripts.csv', script_df[(
    script_df.scenario == scenario)])

transcripts_mean = transcripts.agg(['mean'])
transcripts_mean = transcripts_mean.sort_values(by = 'mean', axis = 1,
ascending = False)
transcripts_mean
# %%

scripts = import_limited_matrices('matrix_scripts.csv', script_df[(
    script_df.scenario == scenario)])

scripts_mean = scripts.agg(['mean'])
scripts_mean = scripts_mean.sort_values(by = 'mean', axis = 1,
ascending = False)
scripts_mean

# %%
