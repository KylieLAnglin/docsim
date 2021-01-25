# %%
import pandas as pd

from docsim.library import start
from docsim.library import process_text
from docsim.library import analyze

# %%

df_corpus = pd.read_csv(start.CLEAN_FILEPATH + "text_transcripts.csv").set_index(
    ["study", "id"]
)
df_ideal = pd.read_csv(start.CLEAN_FILEPATH + "text_scriptsV2.csv").set_index(
    ["study", "id"]
)
df = df_corpus.append(df_ideal)

# %%
