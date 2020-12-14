# %%
import pandas as pd

from docsim.library import start
from docsim.library import qualtrics

# %% Import data
spring2019_path = start.raw_filepath + "Spring_2019/" + "Spring 2019 Coaching Notes.csv"
spring2019_notes = pd.read_csv(spring2019_path)

ids_2018_2019 = pd.read_csv(
    start.raw_filepath + "coaching_notes/" + "Linking Roster 2018.csv"
)

# %% Clean coaching notes

spring2019_notes = qualtrics.select_valid_rows(
    spring2019_notes, keep_previews=True, min_duration=0
)
spring2019_skills = spring2019_notes[["Q37", "Q38", "Q31", "Q41"]].rename(
    columns={"Q37": "name", "Q38": "email", "Q41": "coach", "Q31": "skill_name"}
)

# %% Link coach notes to participant ids
spring2019_skills = spring2019_skills.merge(
    ids_2018_2019[["ID", "Email"]], how="left", left_on="email", right_on="Email"
)  # missing 14/99. These people may have transcripts.
# So these are qualtrics surveys by a coach that do not link to the \
# linking doc with student IDs. Don't know yet how many transcripts don't \
# link to a coach

# %% Label skills
behavior_skill_labels = {
    "Timely redirection": 1,
    "Specific redirection": 2,
    "Succinct redirection": 3,
    "Calm redirection": 4,
}

spring2019_skills["skill"] = spring2019_skills.skill_name.map(behavior_skill_labels)

# %% Save
spring2019_skills.to_csv(start.raw_filepath + "coaching_notes/" + "spring2019_skills")
