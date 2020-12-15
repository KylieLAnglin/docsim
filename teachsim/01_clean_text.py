# %%
import pandas as pd

from docsim.library import start
from docsim.library import clean_text

# %% Import text


# %% Import text and clean
spring2019_filepath = start.raw_filepath + "spring_2019/coaching/"

spring2019_docs = clean_text.import_text(
    filepath=spring2019_filepath, pattern="*docx", paragraph_tag="[New Speaker] "
)

speaker_tags_df = pd.read_csv(
    start.raw_filepath + "spring_2019/Coaching/Spring2019_speaker_tags.csv", header=0
)
temp_dict = speaker_tags_df.set_index("doc").to_dict(orient="index")
speaker_tags = {k: v["coach"] for k, v in temp_dict.items()}

spring2019_docs = {
    k: v.replace(speaker_tags[k], "Coach:") for k, v in spring2019_docs.items()
}


# %%


# In[3]:


def make_text_dict(filepath, pattern):
    os.chdir(filepath)
    doc_text = {}
    for file in os.listdir():
        if fnmatch.fnmatch(file, pattern):
            doc_text[file] = getCoachText(filepath + file)
    return doc_text


def getCoachText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        if len(para.text) > 5:
            new_text = replace_alt_words_for_coach(para.text)
            if new_text[0:6] == "Coach:" or new_text[11:17] == "Coach:":
                new_text = drop_labels(new_text)
                new_text = fix_typos(new_text)
                fullText.append(new_text)
    new_text = " ".join(fullText)
    # new_text = new_text.replace('\\n','')
    return new_text


def replace_alt_words_for_coach(string):
    new_text = string.replace("Instructor:", "Coach:")
    new_text = new_text.replace("Tutor:", "Coach:")
    new_text = new_text.replace("Interviewer:", "Coach:")
    new_text = new_text.replace("Interviewer:", "Coach:")
    new_text = new_text.replace("COACH:", "Coach:")
    new_text = new_text.replace("Interviewer:", "Coach:")
    new_text = new_text.replace("Announcer:", "Coach:")
    new_text = new_text.replace("Female Speaker:", "Coach:")
    new_text = new_text.replace("Male Speaker:", "Coach:")
    new_text = new_text.replace("Arielle:", "Coach:")
    new_text = new_text.replace("Mike Grille:", "Coach:")
    new_text = new_text.replace("Rosalie:", "Coach:")
    new_text = new_text.replace("Moderator:", "Coach:")
    new_text = new_text.replace("Anna Myers:", "Coach:")
    return new_text


def drop_labels(string):
    new_text = string.replace("\\n", "")
    new_text = re.sub(r"\[(.*?)\]", "", new_text)
    new_text = re.sub(r"([a-zA-Z]+)\:", "", new_text)
    return new_text


def fix_typos(string):
    new_text = string.replace("00:00:11]", "")
    new_text = new_text.replace("Dave", "Dev")
    return new_text


def create_df(textdict, year, semester, scenario):
    df = pd.DataFrame.from_dict(data=textdict, orient="index").reset_index()
    df = df.rename({"index": "doc", 0: "text"}, axis="columns")
    df["year"] = year
    df["semester"] = semester
    df["scenario"] = scenario
    df = df.set_index("doc")
    return df


# In[4]:


fall2017_dict = make_text_dict(fall2017_filepath, "*Transcript*")
spring2018_dict = make_text_dict(spring2018_filepath, "*docx")
fall2018_dict = make_text_dict(fall2018_filepath, "2018*docx")
spring2019_dict = make_text_dict(spring2019_filepath, "2019*")
fall2019_dict = make_text_dict(fall2019_filepath, "*Transcript.docx")


# In[5]:


fall2019_dict["01_1920_05_031_22c_Transcript.docx"]


# In[6]:


fall2018_dict["2018_112_3C_Transcript.docx"]


# ## Create dataframe

# In[7]:


fall2017 = create_df(fall2017_dict, "2017-18", "fall", "feedback")
spring2018 = create_df(spring2018_dict, "2017-18", "spring", "behavior")
fall2018 = create_df(fall2018_dict, "2018-19", "fall", "feedback")
spring2019 = create_df(spring2019_dict, "2018-19", "spring", "behavior")
fall2019 = create_df(fall2019_dict, "2019-20", "fall", "behavior")


# %% Add Coaching Notes
# Fall 2017
fall2017["id"] = fall2017.index.str[:-18].astype(int)
fall2017_skills = pd.read_csv(dir + "data/coaching_notes/" + "fall_2017_skills.csv")
fall2017 = (
    fall2017.reset_index()
    .merge(fall2017_skills[["id", "skill"]], how="left", left_on="id", right_on="id")
    .set_index("doc")
)

# Spring 2018
spring2018["id"] = spring2018.index.str[:-8].astype(int)
spring2018_skills = pd.read_csv(dir + "data/coaching_notes/" + "spring_2018_skills.csv")
spring2018 = (
    spring2018.reset_index()
    .merge(spring2018_skills[["id", "skill"]], how="left", left_on="id", right_on="id")
    .set_index("doc")
)

# Fall 2018
fall2018["id"] = fall2018.index.str[5:-19].astype(int)
fall2018_skills = pd.read_csv(dir + "data/coaching_notes/" + "fall_2018_skills.csv")
fall2018_skills2 = pd.DataFrame({"id": [56, 13, 94], "skill": [2, 2, 1]})
fall2018_skills = fall2018_skills.append(fall2018_skills2[["id", "skill"]])

fall2018 = (
    fall2018.reset_index()
    .merge(
        fall2018_skills[["id", "skill", "coach"]],
        how="left",
        left_on="id",
        right_on="id",
        validate="1:1",
    )
    .set_index("doc")
)

# Spring 2019
spring2019["id"] = spring2019.index.str[5:-19].astype(int)
spring2019_skills = pd.read_csv(dir + "data/coaching_notes/" + "spring_2019_skills.csv")
spring2019_skills = spring2019_skills.dropna(axis=0, subset=["skill"])
spring2019_skills2 = pd.DataFrame(
    {
        "id": [16, 119, 7, 25, 40, 30, 10, 84, 89, 113, 87, 106, 54],
        "skill": [4, 2, 2, 3, 2, 2, 3, 2, 2, 3, 3, 2, 4],
    }
)
spring2019_skills = spring2019_skills.append(spring2019_skills2[["id", "skill"]])
spring2019 = (
    spring2019.reset_index()
    .merge(
        spring2019_skills[["id", "skill", "coach"]],
        how="left",
        left_on="id",
        right_on="id",
        validate="1:1",
    )
    .set_index("doc")
)

# Fall 2019
fall2019["id"] = fall2019.index.str[11:-20].astype(int)
fall2019_skills = pd.read_csv(dir + "data/coaching_notes/" + "fall_2019_skills.csv")
fall2019 = (
    fall2019.reset_index()
    .merge(
        fall2019_skills[["id", "skill"]],
        how="left",
        left_on="id",
        right_on="id",
        validate="1:1",
    )
    .set_index("doc")
)


# In[9]:


corpus_df = fall2017.append(spring2018)
corpus_df = corpus_df.append(fall2018)
corpus_df = corpus_df.append(spring2019)
corpus_df = corpus_df.append(fall2019)
corpus_df.sample(10)


# # Send to CSV

# In[10]:


corpus_df.to_csv(clean_filepath + "text_transcripts.csv")


# %%
