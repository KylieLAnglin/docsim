# %%
import pandas as pd


GI_PATH = "/Users/kylie/inquireraugmented.xls"
GI_OUTPUT = "/Users/kylie/generalinquirer.xls"
# %%
gi = pd.read_excel(GI_PATH, skiprows=[1], dtype={"Entry": str})

# %%
gi["word_split"] = [string.split("#", 1) for string in gi.Entry]
gi["word"] = [string[0].lower() for string in gi.word_split]

gi.to_csv(GI_OUTPUT)

# %%
cat_df = gi[gi.Strong == "Strong"]
cat_words = list(cat_df.word.unique())

# %%
