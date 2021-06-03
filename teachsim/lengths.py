# %%
import pandas as pd

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize

from docsim.library import start
from docsim.library import process_text
from docsim.library import analyze
from docsim.library import clean_text

# %%

df = pd.read_csv(start.CLEAN_FILEPATH + "text_transcripts.csv")


df["processed_text"] = [
    process_text.process_text(
        text, lower_case=False, remove_punct=True, remove_stopwords=False, lemma=False
    )
    for text in df.clean_text
]

df["processed_text"] = df.processed_text.str.replace("'", "")

list_of_list_of_tokens = [word_tokenize(text) for text in df.processed_text]

list_of_lengths = [len(tokens) for tokens in list_of_list_of_tokens]

df["word_count"] = list_of_lengths

# %%
print(df[df.study == "spring2018"].word_count.mean())  # 740
print(df[df.study == "spring2019"].word_count.mean())  # 768
print(df[df.study == "fall2019TAP"].word_count.mean())  # 769
print(df[df.study == "fall2017"].word_count.mean())  #
print(df[df.study == "fall2018"].word_count.mean())  #

# %%


print(df[df.study == "spring2018"].word_count.std())  # 133
print(df[df.study == "spring2019"].word_count.std())  # 102
print(df[df.study == "fall2019TAP"].word_count.std())  # 125
print(df[df.study == "fall2017"].word_count.std())  # 136
print(df[df.study == "fall2018"].word_count.std())  #


print(df.word_count.mean())  # 133


# %%