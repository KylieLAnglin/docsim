# %%
import pandas as pd

from docsim.library import start
from docsim.library import qualtrics

SKILLS_PATH = start.RAW_FILEPATH + "coaching_notes/"

TEACHSIM_DATASET_PATH = start.RAW_FILEPATH + "HTE_Outcomes_CPP_Final_Dec2020.dta"

STUDY_SHORT_NAMES = {
    "Fall 2017": "fall2017",
    "Fall 2018": "fall2018",
    "Fall 2019": "fall2019notTAP",
    "Fall 2019 TAP": "fall2019TAP",
    "Spring 2018": "spring2018",
    "Spring 2019": "spring2019",
    "Spring 2020": "spring2020",
}

LINKING_ROSTER_1819_PATH = SKILLS_PATH + "Linking Roster 2018.csv"

BEHAVIOR_SKILL_LABELS = {
    "Timely redirection": "behavior1",
    "Specific redirection": "behavior2",
    "Succinct redirection": "behavior3",
    "Calm redirection": "behavior4",
}

FEEDBACK_SKILL_LABELS = {
    "No coaching conversation, assigned to self reflection": "feedback0",
    "Probing for textual evidence": "feedback1",
    "Scaffolding students' understanding": "feedback2",
    "Providing high-quality descriptive feedback": "feedback3",
    "Probing for a warrant": "feedback4",
}

# %%

# %% Import linking doc
ids_1819 = pd.read_csv(LINKING_ROSTER_1819_PATH).rename(
    columns={"Email": "email", "ID": "id"}
)

# %% Import final analytic TeachSIM dataset
sim_data = pd.read_stata(TEACHSIM_DATASET_PATH, convert_categoricals=False)
sim_data["study"] = sim_data.ma_study.map(STUDY_SHORT_NAMES)

sim_data = sim_data[["id_student", "study", "id_coach"]]
sim_data = sim_data.rename(columns={"id_student": "id", "id_coach": "coach_id"})
sim_data = sim_data.set_index(["study", "id"])

# %% Label skills

behavior_num_to_label = {v: k for k, v in BEHAVIOR_SKILL_LABELS.items()}

feedback_num_to_label = {v: k for k, v in FEEDBACK_SKILL_LABELS.items()}


# %% Fall 2017
skills = pd.read_csv(SKILLS_PATH + "Fall 2017 Skills.csv")
skills["skill"] = "feedback" + skills.Skill.map(str)
skills["skill_name"] = skills.skill.map(feedback_num_to_label)

fall2017 = skills.rename(columns={"Candidate ID": "id"}).drop(columns=["Skill"])

fall2017["study"] = "fall2017"
fall2017 = fall2017.set_index(["study", "id"])

# %% Fall 2018
# Merge coach id to participant id
coach_ids = pd.read_excel(
    SKILLS_PATH + "Linking Roster (Fall 2018).xlsx",
    sheet_name="Linking Roster",
    engine="openpyxl",
)[["ParticipantID", "Session3-4_CoachID_New"]].dropna(how="all")
coach_ids = coach_ids.rename(
    columns={"ParticipantID": "id", "Session3-4_CoachID_New": "coach"}
)
coach_ids["study"] = "fall2018"
coach_ids = coach_ids.set_index(["study", "id"])

# Add skills
notes = pd.read_csv(SKILLS_PATH + "Fall 2018 Coaching Notes.csv")
notes = qualtrics.select_valid_rows(notes, keep_previews=True, min_duration=0)
skills = (
    notes[["Q1", "Q16", "Q6"]].rename(
        columns={"Q1": "name", "Q16": "email", "Q6": "skill_name"}
    )
).dropna(how="all")
skills["skill"] = skills.skill_name.map(FEEDBACK_SKILL_LABELS)

skills = skills.merge(ids_1819[["id", "email"]], how="left", on="email")

skills["study"] = "fall2018"
fall2018 = skills.set_index(["study", "id"])
fall2018 = fall2018.merge(coach_ids, how="left", left_index=True, right_index=True)

# %% Spring 2018
skills = pd.read_csv(SKILLS_PATH + "Spring 2018 Skills.csv")
skills["skill"] = "behavior" + skills.Skill.map(str)
skills["skill_name"] = skills.skill.map(behavior_num_to_label)

spring2018 = skills.rename(columns={"Candidate ID": "id"}).drop(columns=["Skill"])

spring2018["study"] = "spring2018"
spring2018 = spring2018.set_index(["study", "id"])

# %% Spring 2019
notes = pd.read_csv(SKILLS_PATH + "Spring 2019 Coaching Notes.csv")
notes = qualtrics.select_valid_rows(notes, keep_previews=True, min_duration=0)
skills = notes[["Q37", "Q38", "Q31", "Q41"]].rename(
    columns={"Q37": "name", "Q38": "email", "Q41": "coach", "Q31": "skill_name"}
)

# Merge coach notes to participant ids
skills = skills.merge(
    ids_1819[["id", "email"]], how="left", left_on="email", right_on="email"
)  # missing 14/99. These people may have transcripts.
# So these are qualtrics surveys by a coach that do not link to the \
# linking doc with student IDs. Don't know yet how many transcripts don't \
# link to a coach

skills["skill"] = skills.skill_name.map(BEHAVIOR_SKILL_LABELS)
skills = skills.rename(columns={"ID": "id"})[["id", "skill", "skill_name", "coach"]]

spring2019 = skills
spring2019["study"] = "spring2019"
spring2019 = spring2019.dropna(subset=["id"]).set_index(["study", "id"])


# %% Fall 2019 TAP
skills = pd.read_csv(SKILLS_PATH + "Fall 2019 TAP Skills.csv")
skills["skill"] = "behavior" + skills.skill.map(str)
skills["skill_name"] = skills.skill.map(behavior_num_to_label)

fall2019 = skills
fall2019["study"] = "fall2019TAP"
fall2019 = fall2019.set_index(["study", "id"])


# %%
skill_df = pd.concat([fall2017, fall2018, spring2018, spring2019, fall2019])
skill_df = skill_df.merge(sim_data, how="left", left_index=True, right_index=True)
skill_df = skill_df[skill_df.skill != "feedback0"]
# %% Save
skill_df.to_csv(
    start.RAW_FILEPATH + "skills_and_coaches.csv",
)
