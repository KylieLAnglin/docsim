# %%
import pandas as pd

from docsim.library import start
from docsim.library import qualtrics

# %% Fall 2017

# %% Spring 2019
#
# Import and clean coaching notes
path = start.raw_filepath + "Spring_2019/" + "Spring 2019 Coaching Notes.csv"
notes = pd.read_csv(path)
notes = qualtrics.select_valid_rows(notes, keep_previews=True, min_duration=0)
skills = notes[["Q37", "Q38", "Q31", "Q41"]].rename(
    columns={"Q37": "name", "Q38": "email", "Q41": "coach", "Q31": "skill_name"}
)

# Import linking doc
path = start.raw_filepath + "coaching_notes/" + "Linking Roster 2018.csv"
ids = pd.read_csv(path)

# Merge coach notes to participant ids
skills = skills.merge(
    ids[["ID", "Email"]], how="left", left_on="email", right_on="Email"
)  # missing 14/99. These people may have transcripts.
# So these are qualtrics surveys by a coach that do not link to the \
# linking doc with student IDs. Don't know yet how many transcripts don't \
# link to a coach

spring2019 = skills


# %% Label skills
behavior_skill_labels = {
    "Timely redirection": 1,
    "Specific redirection": 2,
    "Succinct redirection": 3,
    "Calm redirection": 4,
}

spring2019_skills["skill"] = spring2019_skills.skill_name.map(behavior_skill_labels)
spring2019_skills = spring2019_skills.set_index("ID")

# %% Save
spring2019_skills.to_csv(
    start.raw_filepath + "coaching_notes/" + "spring2019_skills",
)

# %%
