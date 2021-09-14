# %%
from os import link
import re
import fnmatch

import pandas as pd

from docsim.library import start
from docsim.library import clean_text
from docsim.library import dictionary_tools


# %% Import speaker tags
linking_file = pd.read_csv(start.RAW_FILEPATH + "linking_files.csv", header=0)
speaker_tags_df = linking_file[["filename", "speaker"]].rename(
    columns={"filename": "doc", "speaker": "coach"}
)

speaker_tags_df = speaker_tags_df.dropna()

speaker_tags = speaker_tags_df.set_index("doc").to_dict(orient="index")
speaker_tags = dictionary_tools.fold_nested_dictionary(speaker_tags, "coach")

# import text
filepath = start.RAW_FILEPATH + "transcripts/"

files = [
    filename
    for filename in os.listdir(filepath)
    if fnmatch.fnmatch(filename, "*.docx") and not filename.startswith("~$")
]


# %%
transcripts = list()
for filename in files:
    transcript = clean_text.word_to_transcript(doc_file=filepath + filename)
    transcripts.append(transcript)

    if transcript:
        if filename in list(speaker_tags.keys()):
            transcript_df = clean_text.transcript_to_cleaned_df(transcript=transcript)
            speakers = [
                speaker.replace(speaker_tags[filename].replace(":", ""), "Coach")
                for speaker in transcript_df.speaker
            ]
            transcript_df["speaker"] = speakers

            filename = filename[:-5]
            clean_text.transcript_df_to_excel(
                transcript_df=transcript_df,
                excel_template=start.MAIN_DIR + "template.xlsx",
                excel_file=start.MAIN_DIR
                + "data/excel_transcripts/"
                + filename
                + ".xlsx",
            )


def excel_transcript_to_string(filename: str):
    transcript_df = pd.read_excel(
        filename, dtype={"Time-stamp": str, "Speaker": str, "Text": str}
    )
    transcript_df = transcript_df.fillna("")
    coach_df = transcript_df[transcript_df.Speaker == "Coach"]

    text = " ".join(list(coach_df.Text))
    return text


test = excel_transcript_to_string(
    filename=start.MAIN_DIR
    + "data/excel_transcripts/"
    + "01_1920_01_2593820_22c_Transcript"
    + ".xlsx",
)


files = [
    filename
    for filename in os.listdir(start.MAIN_DIR + "data/excel_transcripts/")
    if fnmatch.fnmatch(filename, "*.xlsx") and not filename.startswith("~$")
]

coach_text = {}
for filename in files:
    print(filename)
    coach_text[filename[:-5] + ".docx"] = excel_transcript_to_string(
        start.MAIN_DIR + "data/excel_transcripts/" + filename,
    )


# fix white space
cleaned_coach_text = {
    k: clean_text.add_whitespace_after_punct(v) for k, v in coach_text.items()
}

# # drop tags
# cleaned_coach_text = {k: re.sub(r"\[(.*?)\]", " ", v) for k, v in coach_text.items()}

# remove hyphens
cleaned_coach_text = {
    k: clean_text.remove_hyphens(v) for k, v in cleaned_coach_text.items()
}
cleaned_dict = {k: [coach_text[k]] + [cleaned_coach_text[k]] for k in coach_text.keys()}


# %%
text_df = pd.DataFrame.from_dict(
    cleaned_dict,
    orient="index",
    columns=["raw_text", "clean_text"],
)

text_df = text_df.merge(linking_file, left_index=True, right_on="filename").rename(
    columns={"person_id": "id"}
)

text_df = text_df[text_df.clean_text != ""]
# %%
text_df.set_index(["study", "id"]).to_csv(start.CLEAN_FILEPATH + "text_transcripts.csv")

# %%
