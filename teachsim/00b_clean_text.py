# %%
from os import link
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
    5. Fix missing white space after periods, question marks, and exclamation points

    Args:
        raw_text_dict (dict): Doc ID as keys, text as values
        speaker_tags_df (pd.DataFrame): filename in "doc" column, coach tag in "coach" column

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

    # remove hyphens
    cleaned_coach_text = {
        k: clean_text.remove_hyphens(v) for k, v in cleaned_coach_text.items()
    }

    new_dict = {k: [raw_text[k]] + [cleaned_coach_text[k]] for k in raw_text.keys()}

    return new_dict


def extract_id_from_dict(dict_with_id: dict, prefix: str, suffix: str):
    new_dict = dictionary_tools.replace_string_key(dict_with_id, prefix, "")
    new_dict = dictionary_tools.replace_string_key(new_dict, suffix, "")
    new_dict = dictionary_tools.string_key_as_int(new_dict)

    return new_dict


def extract_id_from_column(df: pd.DataFrame, prefix: str, suffix: str):
    new_df = df.copy()
    new_df["id"] = new_df.index
    new_df["id"] = new_df.id.str.replace(prefix, "")
    new_df["id"] = new_df.id.str.replace(suffix, "")
    new_df["id"] = new_df["id"].astype(int)

    return new_df


# import text
filepath = start.RAW_FILEPATH + "transcripts/"
raw_text = clean_text.import_text(
    filepath=filepath, pattern="*docx", paragraph_tag="[New Speaker] "
)

# import speaker tags
linking_file = pd.read_csv(start.RAW_FILEPATH + "linking_files.csv", header=0)
speaker_tags_df = linking_file[["filename", "speaker"]].rename(
    columns={"filename": "doc", "speaker": "coach"}
)

speaker_tags_df = speaker_tags_df.dropna()
cleaned_dict = cleaning_protocol(raw_text, speaker_tags_df)

# %%
text_df = pd.DataFrame.from_dict(
    cleaned_dict,
    orient="index",
    columns=["raw_text", "clean_text"],
)

text_df = (
    text_df.merge(linking_file, left_index=True, right_on="filename")
    .rename(columns={"person_id": "id"})
    .set_index(["study", "id"])
)


text_df.to_csv(start.CLEAN_FILEPATH + "text_transcripts.csv")

# %%
