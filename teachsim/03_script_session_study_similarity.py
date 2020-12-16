# %%
import pandas as pd

from docsim.library import start
from docsim.library import analyze

# %%

transcript_df = pd.read_csv(start.clean_filepath + "text_transcripts.csv")
script_df = pd.read_csv(start.clean_filepath + "text_scripts.csv").set_index("id")

df = transcript_df.append(script_df)
df = df[["study", "year", "semester", "scenario", "coach", "skill"]]

matrix = pd.read_csv(start.clean_filepath + "matrix_stop_wgt_lsa.csv")
matrix = matrix.add_prefix("term_")

df = df.merge(matrix, how="left", left_index=True, right_index=True)

# %%
# Script similarity
values = []
for doc in df[df.study == "spring2019"].index:
    value = analyze.max_sim_of_rows(
        df[list(df.filter(regex=("term")))],
        doc,
        list(df[(df.study == "model") & (df.scenario == "behavior")].index),
    )
    values.append(value)


def max_sim(transcript_matrix, script_matrix):
    sims_df = pd.DataFrame({"doc": transcript_matrix.index.tolist()}).set_index("doc")
    for script in script_matrix.index:
        sims = distance_to_doc(transcript_matrix, script_matrix.loc[script])
        sims_df[script] = sims

    sims_df["script_sim"] = sims_df[script_matrix.index.tolist()].max(axis=1)

    return sims_df[["script_sim"]]


script_results = pd.DataFrame()
for scenario in ["feedback", "behavior"]:
    for skill in [1, 2, 3, 4]:
        sim_df = script_similarity(
            matrix_transcripts_file="matrix_transcripts.csv",
            limited_transcript_df=transcript_df[
                ((transcript_df.scenario == scenario) & (transcript_df.skill == skill))
            ],
            matrix_scripts_file="matrix_scripts.csv",
            limited_script_df=script_df[
                (script_df.scenario == scenario) & (script_df.skill == skill)
            ],
        )
        script_results = script_results.append(sim_df)


results = results.merge(script_results, left_index=True, right_index=True)
results.to_csv((clean_filepath + "results.csv"))


# %%
def distance_to_mean(matrix_main, matrix_comparison):
    sims = []
    for maindoc in matrix_main.index:
        matrix_comp = matrix_comparison[
            ~matrix_comparison.index.isin([maindoc])
        ]  # exclude self
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
        matrix_comp = matrix_comparison[
            ~matrix_comparison.index.isin([maindoc])
        ]  # exclude self
        for compdoc in matrix_comp.index:
            sim = 1 - spatial.distance.cosine(
                matrix_main.loc[maindoc], matrix_comp.loc[compdoc]
            )
            sims.append(sim)
        ave_sim = sum(sims) / len(sims)
        ave_sims.append(ave_sim)
    return ave_sims


def session_similarity(matrix_transcripts_file, text_df):
    """
    Creates new variable for text_df containing session similarity.
    Returns new df with variable.
    """
    matrix_transcripts = pd.read_csv(clean_filepath + matrix_transcripts_file)
    matrix_transcripts = matrix_transcripts.set_index("doc")
    results = text_df[(text_df.year == "2017-18") & (text_df.semester == "fall")]
    matrix = matrix_transcripts[matrix_transcripts.index.isin(results.index)]
    sims = pairwise_distance(matrix, matrix)
    results["session_sim"] = sims
    semesters = ["spring", "fall", "spring", "fall"]
    years = ["2017-18", "2018-19", "2018-19", "2019-20"]
    for semester, year in zip(semesters, years):
        df = text_df[(text_df.year == year) & (text_df.semester == semester)]
        matrix = matrix_transcripts[matrix_transcripts.index.isin(df.index)]
        sims = pairwise_distance(matrix, matrix)
        df["session_sim"] = sims
        results = results.append(df)
    return results


def study_similarity(matrix_transcripts_file, text_df):
    """
    Calculates the distance of every document to the mean of every study.
    Returns new df with variable for every study distance.
    """
    semesters = ["fall", "spring", "fall", "spring", "fall"]
    years = ["2017-18", "2017-18", "2018-19", "2018-19", "2019-20"]

    matrix_transcripts = pd.read_csv(clean_filepath + matrix_transcripts_file)
    matrix_transcripts = matrix_transcripts.set_index("doc")

    for semester, year in zip(semesters, years):
        matrix = matrix_transcripts

        comp = text_df[(text_df.year == year) & (text_df.semester == semester)]
        matrix_comp = matrix_transcripts[matrix_transcripts.index.isin(comp.index)]

        sims = pairwise_distance(matrix, matrix_comp)
        results["study_sim_" + semester + year[0:4] + "_" + year[5:7]] = sims
    return results


def script_similarity(
    matrix_transcripts_file,
    limited_transcript_df,
    matrix_scripts_file,
    limited_script_df,
):
    # limit transcripts
    transcript_matrix = import_limited_matrices(
        matrix_transcripts_file, limited_transcript_df
    )

    # limit scripts
    script_matrix = import_limited_matrices(matrix_scripts_file, limited_script_df)

    sims_df = max_sim(transcript_matrix=transcript_matrix, script_matrix=script_matrix)

    return sims_df


def max_sim(transcript_matrix, script_matrix):
    sims_df = pd.DataFrame({"doc": transcript_matrix.index.tolist()}).set_index("doc")
    for script in script_matrix.index:
        sims = distance_to_doc(transcript_matrix, script_matrix.loc[script])
        sims_df[script] = sims

    sims_df["script_sim"] = sims_df[script_matrix.index.tolist()].max(axis=1)

    return sims_df[["script_sim"]]


def import_limited_matrices(matrix_file: str, limited_text_df: pd.DataFrame):
    matrix = pd.read_csv(clean_filepath + matrix_file)
    matrix = matrix.set_index("doc")

    # limit to scenario scripts
    limited_matrix = matrix[matrix.index.isin(limited_text_df.index)]

    return limited_matrix


# %%
# No pre-processing
results = session_similarity("matrix_transcripts.csv", transcript_df)  # session sim col
results = study_similarity(
    "matrix_transcripts.csv", transcript_df
)  # creates study sim cols

script_results = pd.DataFrame()
for scenario in ["feedback", "behavior"]:
    for skill in [1, 2, 3, 4]:
        sim_df = script_similarity(
            matrix_transcripts_file="matrix_transcripts.csv",
            limited_transcript_df=transcript_df[
                ((transcript_df.scenario == scenario) & (transcript_df.skill == skill))
            ],
            matrix_scripts_file="matrix_scripts.csv",
            limited_script_df=script_df[
                (script_df.scenario == scenario) & (script_df.skill == skill)
            ],
        )
        script_results = script_results.append(sim_df)


results = results.merge(script_results, left_index=True, right_index=True)
results.to_csv((clean_filepath + "results.csv"))

# %%
techniques = [
    "_stop",
    "_stop_wgt",
    "_stem",
    "_stem_stop",
    "_stem_stop_wgt",
    "_lsa",
    "_lsa_stop",
    "_lsa_wgt_stop",
]
for tech in techniques:
    matrix_transcripts_file = "matrix_transcripts" + tech + ".csv"
    matrix_scripts_file = "matrix_scripts" + tech + ".csv"
    results = session_similarity(matrix_transcripts_file, transcript_df)
    results = study_similarity(matrix_transcripts_file, transcript_df)

    script_results = pd.DataFrame()
    for scenario in ["feedback", "behavior"]:
        for skill in [1, 2, 3, 4]:
            sim_df = script_similarity(
                matrix_transcripts_file=matrix_transcripts_file,
                limited_transcript_df=transcript_df[
                    (
                        (transcript_df.scenario == scenario)
                        & (transcript_df.skill == skill)
                    )
                ],
                matrix_scripts_file=matrix_scripts_file,
                limited_script_df=script_df[
                    (script_df.scenario == scenario) & (script_df.skill == skill)
                ],
            )
            script_results = script_results.append(sim_df)

    results = results.merge(script_results, left_index=True, right_index=True)
    results.to_csv((clean_filepath + "results" + tech + ".csv"))


# %%
