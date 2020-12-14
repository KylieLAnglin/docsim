# %%
import pandas as pd

from docsim.library import start


# %% Imports

spring_2019_notes = pd.read_csv(start.raw_filepath + 'Spring_2019/' + 'Spring 2019 Coaching Notes.csv')
spring_2019_notes = spring_2019_notes[['Q37', 'Q38', 'Q31', 'Q41']]

# %% Merges and clean
feedback_skill_labels = {'No coaching conversation, assigned to self reflection': 0,
                         "Probing for textual evidence": 1,
                         "Scaffolding students' understanding": 2,
                         "Providing high-quality descriptive feedback": 3,
                         "Probing for a warrant": 4}

behavior_skill_labels = {"Timely redirection": 1,
                         "Specific redirection": 2,
                         "Succinct redirection": 3,
                         "Calm redirection": 4}


fall_2018_skills = fall_2018_notes.merge(ids_2018_2019, how='inner',
                                         left_on='Q16', right_on='Email',
                                         indicator=True)
fall_2018_skills['Skill'] = fall_2018_skills['Q6'].map(feedback_skill_labels)
fall_2018_skills = fall_2018_skills[['ID', 'Skill']]
fall_2018_skills = fall_2018_skills.rename(
    columns={'ID': 'id', 'Skill': 'skill'})
fall_2018_skills = fall_2018_skills.merge(coach_ids_fall2018, how='inner',
                                          left_on='id', right_on='id')


spring_2019_skills = spring_2019_notes.merge(ids_2018_2019, how='inner',
                                             left_on='Q38', right_on='Email',
                                             indicator=True)
spring_2019_skills['Skill'] = spring_2019_skills['Q31'].map(
    behavior_skill_labels)
spring_2019_skills = spring_2019_skills[['ID', 'Skill', 'Q41']]
spring_2019_skills = spring_2019_skills.rename(
    columns={'ID': 'id', 'Skill': 'skill', 'Q41': 'coach'})

# %% Exports

for df, file in zip([fall_2017_skills, spring_2018_skills,
                     fall_2018_skills, spring_2019_skills, fall_2019_skills],
                    ['fall_2017_skills.csv', 'spring_2018_skills.csv',
                     'fall_2018_skills.csv', 'spring_2019_skills.csv',
                     'fall_2019_skills.csv']):

    df.to_csv(skills_path + file)


# %%
