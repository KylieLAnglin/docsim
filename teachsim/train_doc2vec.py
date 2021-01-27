# %%
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import gensim

# %%
import pandas as pd

from docsim.library import start
from docsim.library import process_text
from docsim.library import analyze
from docsim.library import clean_text

# %%

df_corpus = pd.read_csv(start.CLEAN_FILEPATH + "text_transcripts.csv")
df_ideal = pd.read_csv(start.CLEAN_FILEPATH + "text_scriptsV2.csv")
df = df_corpus.append(df_ideal)

df["filename"] = df.filename.str.replace(".docx", "")
df["filename"] = df.filename.str.replace("_Transcript", "")

df = df.set_index("filename")

# %%

data = list(df.clean_text)
tagged_data = [
    TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)])
    for i, _d in enumerate(data)
]

model = Doc2Vec(tagged_data, dm=1)


# %%
MAX_EPOCHS = 100


# model.build_vocab(tagged_data)

# for epoch in range(MAX_EPOCHS):
#     print("iteration {0}".format(epoch))
#     model.train(tagged_data, total_examples=model.corpus_count, epochs=model.iter)
#     # decrease the learning rate
#     model.alpha -= 0.0002
#     # fix the learning rate, no decay
#     model.min_alpha = model.alpha

model.save(start.CLEAN_FILEPATH + "doc2vec.model")
print("Model Saved")

# %%
