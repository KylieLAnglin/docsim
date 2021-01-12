# %%
import re

import pandas as pd

from docsim.library import start
from docsim.library import clean_text
from docsim.library import dictionary_tools

# %%
def cleaning_protocol(raw_text_dict: dict, speaker_tags_df: pd.DataFrame):
    """Cleans transcripts from dict and returned cleaned dict

    1. Make consistent coach tags
    2. Only keep coach text
    3. Drop tags in brackets
    4. Drop coach tags

    Args:
        raw_text_dict (dict): Doc ID as keys, text as values
        speaker_tags_df (pd.DataFrame): Doc ID in col 1, previous coach tag in col 2

    Returns:
        [dict]: Doc ID as keys, cleaned text as values
    """

    temp_dict = speaker_tags_df.set_index("doc").to_dict(orient="index")
    speaker_tags = dictionary_tools.fold_nested_dictionary(temp_dict, "coach")

    # clean speaker tags
    cleaned_speaker_text = {
        k: v.replace(speaker_tags[k], "Coach:") for k, v in raw_text_dict.items()
    }

    # only keep coach text
    coach_text = {
        k: clean_text.filter_segments(v, "[New Speaker]", filter_tag="Coach:")
        for k, v in cleaned_speaker_text.items()
    }
    # drop tags
    cleaned_coach_text = {
        k: re.sub(r"\[(.*?)\]", " ", v) for k, v in coach_text.items()
    }

    # drop coach speaker tag
    cleaned_coach_text = {
        k: re.sub(r"Coach:", " ", v) for k, v in cleaned_coach_text.items()
    }

    # fix white space
    cleaned_coach_text = {
        k: clean_text.add_whitespace_after_punct(v)
        for k, v in cleaned_coach_text.items()
    }

    new_dict = {k: [raw_text[k]] + [cleaned_coach_text[k]] for k in raw_text.keys()}

    return new_dict


def extract_id(dict_with_id: dict, prefix: str, suffix: str):
    new_dict = dictionary_tools.replace_string_key(dict_with_id, prefix, "")
    new_dict = dictionary_tools.replace_string_key(new_dict, suffix, "")
    new_dict = dictionary_tools.string_key_as_int(new_dict)

    return new_dict


# %% Fall 2017

# import text
filepath = start.raw_filepath + "fall_2017/coaching/"
raw_text = clean_text.import_text(
    filepath=filepath, pattern="*docx", paragraph_tag="[New Speaker] "
)

# import speaker tags
speaker_tags_df = pd.read_csv(filepath + "fall2017_speaker_tags.csv", header=0)

cleaned_dict = cleaning_protocol(raw_text, speaker_tags_df)

cleaned_dict = extract_id(cleaned_dict, prefix="", suffix="_c_Transcript.docx")

text_df = pd.DataFrame.from_dict(
    cleaned_dict,
    orient="index",
    columns=["raw_text", "clean_text"],
)
text_df["study"] = "fall2017"
text_df["year"] = 2017
text_df["semester"] = "fall"
text_df["scenario"] = "feedback"
text_df = text_df.reset_index().rename(columns={"index": "id"}).set_index("id")
fall2017 = text_df

# %% Spring 2018

# import text
filepath = start.raw_filepath + "spring_2018/coaching/"
raw_text = clean_text.import_text(
    filepath=filepath, pattern="*docx", paragraph_tag="[New Speaker] "
)

# import speaker tags
speaker_tags_df = pd.read_csv(filepath + "spring2018_speaker_tags.csv", header=0)

cleaned_dict = cleaning_protocol(raw_text, speaker_tags_df)

cleaned_dict = extract_id(cleaned_dict, prefix="", suffix="-2C.docx")

text_df = pd.DataFrame.from_dict(
    cleaned_dict,
    orient="index",
    columns=["raw_text", "clean_text"],
)
text_df["study"] = "spring2018"
text_df["year"] = 2018
text_df["semester"] = "spring"
text_df["scenario"] = "behavior"
text_df = text_df.reset_index().rename(columns={"index": "id"}).set_index("id")
spring2018 = text_df

# %% Fall 2018

# import text
filepath = start.raw_filepath + "fall_2018/coaching/"
raw_text = clean_text.import_text(
    filepath=filepath, pattern="*docx", paragraph_tag="[New Speaker] "
)

# import speaker tags
speaker_tags_df = pd.read_csv(filepath + "fall2018_speaker_tags.csv", header=0)

cleaned_dict = cleaning_protocol(raw_text, speaker_tags_df)

cleaned_dict = extract_id(cleaned_dict, prefix="2018_", suffix="_3C_Transcript.docx")

text_df = pd.DataFrame.from_dict(
    cleaned_dict,
    orient="index",
    columns=["raw_text", "clean_text"],
)
text_df["study"] = "fall2018"
text_df["year"] = 2018
text_df["semester"] = "fall"
text_df["scenario"] = "feedback"
text_df = text_df.reset_index().rename(columns={"index": "id"}).set_index("id")
fall2018 = text_df

# %% Spring2019

# import text
filepath = start.raw_filepath + "spring_2019/coaching/"
raw_text = clean_text.import_text(
    filepath=filepath, pattern="*docx", paragraph_tag="[New Speaker] "
)

# import speaker tags
speaker_tags_df = pd.read_csv(filepath + "Spring2019_speaker_tags.csv", header=0)

cleaned_dict = cleaning_protocol(raw_text, speaker_tags_df)

cleaned_dict = extract_id(cleaned_dict, prefix="2019_", suffix="_5C_Transcript.docx")

text_df = pd.DataFrame.from_dict(
    cleaned_dict,
    orient="index",
    columns=["raw_text", "clean_text"],
)
text_df["study"] = "spring2019"
text_df["year"] = 2019
text_df["semester"] = "spring"
text_df["scenario"] = "behavior"
text_df = text_df.reset_index().rename(columns={"index": "id"}).set_index("id")
spring2019 = text_df

# %% Fall 2019 TAP

# import text
filepath = start.raw_filepath + "fall_2019_TAP/coaching/"
raw_text = clean_text.import_text(
    filepath=filepath, pattern="*docx", paragraph_tag="[New Speaker] "
)

# import speaker tags
speaker_tags_df = pd.read_csv(filepath + "fall2019TAP_speaker_tags.csv", header=0)

cleaned_dict = cleaning_protocol(raw_text, speaker_tags_df)

cleaned_dict = extract_id(
    cleaned_dict, prefix="01_1920_05_", suffix="_22c_Transcript.docx"
)

text_df = pd.DataFrame.from_dict(
    cleaned_dict,
    orient="index",
    columns=["raw_text", "clean_text"],
)
text_df["study"] = "fall2019TAP"
text_df["year"] = 2019
text_df["semester"] = "fall"
text_df["scenario"] = "behavior"
text_df = text_df.reset_index().rename(columns={"index": "id"}).set_index("id")
fall2019TAP = text_df

# %% Concatenate
df = pd.concat([fall2017, spring2018, fall2018, spring2019, fall2019TAP])
df = df.reset_index().set_index(["study", "id"])

# %% Merge skills
skills = pd.read_csv(
    start.raw_filepath + "coaching_notes/" + "skills_and_coaches.csv",
    index_col=["study", "id"],
)

df = df.merge(skills, how="left", left_index=True, right_index=True)


df.to_csv(start.clean_filepath + "text_transcripts.csv")

# %%
