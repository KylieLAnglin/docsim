# %%
import re

import pandas as pd

from docsim.library import start
from docsim.library import clean_text

# %% Functions
def fold_nested_dictionary(input_dict: dict, inner_key: str):
    """Given an input dictionary with keys mapping to inner dictionaries, extract
        the value of some common key to the inner dictionary and return the new
        "folded" dictionary.

    Arguments:
        input_dict (Dict[Any, Dict[str, Any]]): The input dictionary containing dictionaries as values
        inner_key (str): The key to use to extract a given value out of the inner dictionaries.

    Returns:
        A new "folded" dictionary consisting of the original dictionary's keys and the values of the inner_key.
    """
    return {k: v[inner_key] for k, v in input_dict.items()}


def replace_string_value_as_list(input_dict: dict):
    """Given an input dictionary, replace string values with list of one string

    Args:
        input_dict (dict): Dictionary containing string values

    Returns:
        [type]: Dictionary containing list values of one item each
    """
    return {k: [v] for k, v in input_dict.items()}


# %% Import text and clean


spring2019_filepath = start.raw_filepath + "spring_2019/coaching/"

raw_text = clean_text.import_text(
    filepath=spring2019_filepath, pattern="*docx", paragraph_tag="[New Speaker] "
)

speaker_tags_df = pd.read_csv(
    spring2019_filepath + "Spring2019_speaker_tags.csv", header=0
)
temp_dict = speaker_tags_df.set_index("doc").to_dict(orient="index")
speaker_tags = fold_nested_dictionary(temp_dict, "coach")


cleaned_speaker_text = {
    k: v.replace(speaker_tags[k], "Coach:") for k, v in raw_text.items()
}

coach_text = {
    k: clean_text.filter_segments(v, "[New Speaker]", filter_tag="Coach:")
    for k, v in cleaned_speaker_text.items()
}
cleaned_coach_text = {k: re.sub(r"\[(.*?)\]", " ", v) for k, v in coach_text.items()}
cleaned_coach_text = {
    k: re.sub(r"Coach:", " ", v) for k, v in cleaned_coach_text.items()
}


# combine dictionaries
big_dict = {k: [raw_text[k]] + [cleaned_coach_text[k]] for k in raw_text.keys()}

text_df = pd.DataFrame.from_dict(
    big_dict,
    orient="index",
    columns=["raw_text", "clean_text"],
)
text_df["year"] = 2019
text_df["semester"] = "spring"
text_df["scenario"] = "behavior"
text_df = text_df.reset_index().rename(columns={"index": "doc"})
# %%

text_df.to_csv(start.clean_filepath + "text_transcripts.csv", index=False)
