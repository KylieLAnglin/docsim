# %%
import pandas as pd

dir = '/Users/kylie/docsim/'
skills_path = dir + 'data/coaching_notes/'

# %% Imports
fall_2017_skills = pd.read_csv(skills_path + 'Fall 2017 Skills.csv')
fall_2017_skills = fall_2017_skills.rename(columns={'Candidate ID': 'id',
                                                    'Skill': 'skill'})

spring_2018_skills = pd.read_csv(skills_path + 'Spring 2018 Skills.csv')
spring_2018_skills = spring_2018_skills.rename(columns={'Candidate ID': 'id',
                                                        'Skill': 'skill'})

fall_2018_notes = pd.read_csv(skills_path + 'Fall 2018 Coaching Notes.csv')
fall_2018_notes = fall_2018_notes[['Q1', 'Q16', 'Q6']]

spring_2019_notes = pd.read_csv(skills_path + 'Spring 2019 Coaching Notes.csv')
spring_2019_notes = spring_2019_notes[['Q37', 'Q38', 'Q31', 'Q41']]

fall_2019_skills = pd.read_csv(skills_path + 'Fall 2019 TAP Skills.csv')

ids_2018_2019 = pd.read_csv(skills_path + 'Linking Roster 2018.csv')

coach_ids_fall2018 = pd.read_excel(skills_path + 'Linking Roster (Fall 2018).xlsx',
                                   sheet_name=0)
coach_ids_fall2018 = coach_ids_fall2018[[
    'ParticipantID', 'Session3-4_CoachID_New']]
coach_ids_fall2018 = coach_ids_fall2018.rename(columns={'ParticipantID': 'id',
                                                        'Session3-4_CoachID_New': 'coach'})

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
