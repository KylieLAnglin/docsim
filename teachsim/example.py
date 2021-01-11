# %%
# %%
import pandas as pd
from docsim.library import process_text
from docsim.library import analyze


pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)


# %%

text1 = "I can be a good friend by sharing my toys. Sharing means giving a toy to a friend so that they can play with it. I can say here you go and hand them the toy"
text2 = "Sharing means playing with toys at the same time as another friend. We can play together. I can ask can I play with you."

example_df = pd.DataFrame(
    {
        "doc": ["A", "B"],
        "text": [text1, text2],
    }
).set_index(["doc"])

# %%
matrix = process_text.vectorize_text(example_df, "text")

print(analyze.cosine_similarity_row(matrix, "A", "B"))

process_text.process_text(text1, lower_case=True, remove_punct=True)
process_text.process_text(text2, lower_case=True, remove_punct=True)

# %%
matrix = process_text.vectorize_text(example_df, "text", remove_stopwords=True)

print(analyze.cosine_similarity_row(matrix, "A", "B"))

process_text.process_text(text1, lower_case=True, remove_punct=True, remove_stopwords=True)
process_text.process_text(text2, lower_case=True, remove_punct=True, remove_stopwords=True)
# %%


matrix = process_text.vectorize_text(example_df, "text", remove_stopwords=True, lemma=True)

print(analyze.cosine_similarity_row(matrix, "A", "B"))

process_text.process_text(text1, lower_case=True, remove_punct=True, remove_stopwords=True, lemma=True)
process_text.process_text(text2, lower_case=True, remove_punct=True, remove_stopwords=True, lemma=True)

# %%
