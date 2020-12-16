# %%
import re

import pandas as pd

from docsim.library import start
from docsim.library import clean_text
from docsim.library import dictionary_tools

# %% Import text and clean


spring2019_filepath = start.raw_filepath + "spring_2019/coaching/"

raw_text = clean_text.import_text(
    filepath=spring2019_filepath, pattern="*docx", paragraph_tag="[New Speaker] "
)

speaker_tags_df = pd.read_csv(
    spring2019_filepath + "Spring2019_speaker_tags.csv", header=0
)
temp_dict = speaker_tags_df.set_index("doc").to_dict(orient="index")
speaker_tags = dictionary_tools.fold_nested_dictionary(temp_dict, "coach")


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

# %%

# combine dictionaries
big_dict = {k: [raw_text[k]] + [cleaned_coach_text[k]] for k in raw_text.keys()}
big_dict = dictionary_tools.replace_string_key(big_dict, "2019_", "")
big_dict = dictionary_tools.replace_string_key(big_dict, "_5C_Transcript.docx", "")
big_dict = dictionary_tools.string_key_as_int(big_dict)

# %%

text_df = pd.DataFrame.from_dict(
    big_dict,
    orient="index",
    columns=["raw_text", "clean_text"],
)
text_df["study"] = "spring2019"
text_df["year"] = 2019
text_df["semester"] = "spring"
text_df["scenario"] = "behavior"
text_df = text_df.reset_index().rename(columns={"index": "id"}).set_index("id")

# %% Merge skills
skills = pd.read_csv(
    start.raw_filepath + "coaching_notes/" + "spring2019_skills", index_col="ID"
)

text_df = text_df.merge(skills, left_index=True, right_index=True)
text_df = text_df.reset_index().rename(columns={"index": "id"}).set_index("id")

# %%


text_df.to_csv(start.clean_filepath + "text_transcripts.csv")

# %%
