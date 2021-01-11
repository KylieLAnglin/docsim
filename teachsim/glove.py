# %%
# %%
import pandas as pd

from docsim.library import start
from docsim.library import process_text


def loadGloveModel(File):
    print("Loading Glove Model")
    f = open(File, "r")
    gloveModel = {}
    for line in f:
        splitLines = line.split()
        word = splitLines[0]
        wordEmbedding = np.array([float(value) for value in splitLines[1:]])
        gloveModel[word] = wordEmbedding
    print(len(gloveModel), " words loaded!")
    return gloveModel


# %%

df_corpus = pd.read_csv(start.clean_filepath + "text_transcripts.csv").set_index(
    ["study", "id"]
)
df_ideal = pd.read_csv(start.clean_filepath + "text_scripts.csv").set_index(
    ["study", "id"]
)
df = df_corpus.append(df_ideal)
