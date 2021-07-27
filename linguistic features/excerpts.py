# %%
import pandas as pd
import nltk
from docsim.library import process_text

gi = pd.read_csv("/Users/kylie/generalinquirer.xls")
# %%
PATH = "/Users/kylie/Dropbox/Active/docsim/data/excerpts"

files = []
texts = []
for filename in os.listdir(PATH):
    if ".txt" in filename:
        text = open(PATH + "/" + filename, "r").read()
        files.append(filename)
        texts.append(text)

df = pd.DataFrame(list(zip(files, texts)), columns=["Filename", "text"])


df["text_lemmatized"] = [
    process_text.process_text_nltk(text, lower_case=True, remove_punct=True, lemma=True)
    for text in df.text
]

df["lemmas"] = [
    process_text.process_text_nltk(
        text, lower_case=True, remove_punct=True, lemma=True, string_or_list="list"
    )
    for text in df.text
]


# %% import TAACO results
taaco = pd.read_csv(
    "/Users/kylie/Dropbox/Active/docsim/data/excerpts/excerpt_results.csv"
)
taaco = taaco[
    [
        "Filename",
        "lemma_ttr",
        "adjacent_overlap_all_sent",
        "word2vec_1_all_sent",
        "coordinating_conjuncts",
        "all_causal",
    ]
]

df = df.merge(taaco, on=["Filename"], how="inner")
# %%
def determine_tense_input(sentence: str, tense_to_return: str):
    text = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(text)

    tense = {}
    tense["future"] = len([word for word in tagged if word[1] == "MD"])
    tense["present"] = len(
        [word for word in tagged if word[1] in ["VBP", "VBZ", "VBG"]]
    )
    tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
    verb_tense = tense[tense_to_return]
    return verb_tense


df["past"] = [determine_tense_input(text, "past") for text in df.text]
df["present"] = [determine_tense_input(text, "present") for text in df.text]
df["future"] = [determine_tense_input(text, "future") for text in df.text]


# %% General inquirer
def count_words_in_dict(list_of_words: list, dictionary_list: list):
    return len([i for i in list_of_words if i in dictionary_list])


def gi_search(gi_cat: str, df: pd.DataFrame):
    temp_df = gi.copy()
    temp_df = temp_df.rename(columns={gi_cat: "gi_cat"})
    cat_word_list = list(temp_df[temp_df.gi_cat == gi_cat].word.unique())

    cat_words = [set([i for i in lemmas if i in cat_word_list]) for lemmas in df.lemmas]

    cat_word_count = [
        count_words_in_dict(lemmas, cat_word_list) for lemmas in df.lemmas
    ]

    return (cat_words, cat_word_count)


df["strong_words"] = gi_search("Strong", df)[0]
df["strong_word_count"] = gi_search("Strong", df)[1]


df["weak_words"] = gi_search("Weak", df)[0]
df["weak_word_count"] = gi_search("Weak", df)[1]

df["active_words"] = gi_search("Active", df)[0]
df["active_word_count"] = gi_search("Active", df)[1]

df["passive_words"] = gi_search("Passive", df)[0]
df["passive_word_count"] = gi_search("Passive", df)[1]

df["goal_words"] = gi_search("Goal", df)[0]
df["goal_word_count"] = gi_search("Goal", df)[1]

# %%

df.to_csv("/Users/kylie/Dropbox/Active/docsim/excerpt_description.csv")