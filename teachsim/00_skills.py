# %%
import pandas as pd

from docsim.library import start
from docsim.library import qualtrics

skills_path = start.raw_filepath + "coaching_notes/"

# Import linking doc
path = start.raw_filepath + "coaching_notes/" + "Linking Roster 2018.csv"
ids_1819 = pd.read_csv(path)

# %% Label skills
behavior_skill_labels = {
    "Timely redirection": "behavior1",
    "Specific redirection": "behavior2",
    "Succinct redirection": "behavior3",
    "Calm redirection": "behavior4",
}

behavior_num_to_label = {v: k for k, v in behavior_skill_labels.items()}

feedback_skill_labels = {
    "No coaching conversation, assigned to self reflection": "feedback0",
    "Probing for textual evidence": "feedback1",
    "Scaffolding students' understanding": "feedback2",
    "Providing high-quality descriptive feedback": "feedback3",
    "Probing for a warrant": "feedback4",
}

feedback_num_to_label = {v: k for k, v in feedback_skill_labels.items()}

# %% Fall 2017

skills = pd.read_csv(skills_path + "Fall 2017 Skills.csv")
skills["skill"] = "feedback" + skills.Skill.map(str)
skills["skill_name"] = skills.skill.map(feedback_num_to_label)

fall2017 = skills.rename(columns={"Candidate ID": "id"}).drop(columns=["Skill"])

fall2017["study"] = "fall2017"
fall2017 = fall2017.set_index(["study", "id"])

# %% Spring 2018
skills = pd.read_csv(skills_path + "Spring 2018 Skills.csv")
skills["skill"] = "behavior" + skills.Skill.map(str)
skills["skill_name"] = skills.skill.map(behavior_num_to_label)

spring2018 = skills.rename(columns={"Candidate ID": "id"}).drop(columns=["Skill"])

spring2018["study"] = "spring2018"
spring2018 = spring2018.set_index(["study", "id"])

# %% Fall 2018
notes = pd.read_csv(skills_path + "Fall 2018 Coaching Notes.csv")
notes = qualtrics.select_valid_rows(notes, keep_previews=True, min_duration=0)
skills = notes[["Q1", "Q16", "Q6"]].rename(
    columns={"Q1": "name", "Q16": "email", "Q6": "skill_name"}
)
# skills["skill"] = "feedback" + skills.skill.map(str)

# Merge coach notes to participant ids
skills = skills.merge(
    ids_1819[["ID", "Email"]], how="left", left_on="email", right_on="Email"
)

skills["skill"] = skills.skill_name.map(feedback_skill_labels)


fall2018 = skills.rename(columns={"ID": "id"})[["id", "skill", "skill_name"]]

fall2018["study"] = "fall2018"
fall2018 = fall2018.set_index(["study", "id"])

# %% Spring 2019

notes = pd.read_csv(skills_path + "Spring 2019 Coaching Notes.csv")
notes = qualtrics.select_valid_rows(notes, keep_previews=True, min_duration=0)
skills = notes[["Q37", "Q38", "Q31", "Q41"]].rename(
    columns={"Q37": "name", "Q38": "email", "Q41": "coach", "Q31": "skill_name"}
)

# Merge coach notes to participant ids
skills = skills.merge(
    ids[["ID", "Email"]], how="left", left_on="email", right_on="Email"
)  # missing 14/99. These people may have transcripts.
# So these are qualtrics surveys by a coach that do not link to the \
# linking doc with student IDs. Don't know yet how many transcripts don't \
# link to a coach

skills["skill"] = skills.skill_name.map(behavior_skill_labels)
skills = skills.rename(columns={"ID": "id"})[["id", "skill", "skill_name", "coach"]]

spring2019 = skills
spring2019["study"] = "spring2019"
spring2019 = spring2019.set_index(["study", "id"])

# %% Fall 2019
skills = pd.read_csv(skills_path + "Fall 2019 TAP Skills.csv")
skills["skill"] = "behavior" + skills.skill.map(str)
skills["skill_name"] = skills.skill.map(behavior_num_to_label)

fall2019 = skills
fall2019["study"] = "fall2019TAP"
fall2019 = fall2019.set_index(["study", "id"])


# %%
skill_df = pd.concat([fall2017, fall2018, spring2018, spring2019, fall2019])

# %% Save
skill_df.to_csv(
    start.raw_filepath + "coaching_notes/" + "skills_and_coaches.csv",
)
