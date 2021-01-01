# %%
import pandas as pd
from docsim.library import vectorize
from docsim.library import analyze


pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

# %%
example_df = pd.DataFrame(
    {
        "doc": ["script", "good", "bad"],
        "text": [
            "One thing that made me so excited is that I saw you acknowledged every time a student misbehaved. That is so important because it shows me that you already have the lens to recognize misbehavior as soon as it begins.",
            "One thing that I think you did a really nice job with. Every time there was some sort of a misbehavior, whether it was off task chatter or humming, you always acknowledge that and that like can sound like kind of silly - but it's important to acknowledge the behavior.",
            "In this five minutes things are escalating a lot. And then even when you're substituting, like students they're going to- They're going to push the buttons and misbehave. So, you almost want to think about, like I'm cutting it down now.",
        ],
    }
)
example_df = example_df.set_index("doc")

# %%
matrix = vectorize.vectorize_text(example_df, "text")
matrix = matrix.sort_values("script", axis=1, ascending=False)
matrix = matrix.reindex(matrix.mean().sort_values(ascending=False).index, axis=1)
matrix

print(analyze.cosine_similarity_row(matrix, "script", "good"))
print(analyze.cosine_similarity_row(matrix, "script", "bad"))
print(analyze.cosine_similarity_row(matrix, "bad", "good"))


# %%
matrix = vectorize.vectorize_text(example_df, "text", remove_stopwords=True)
matrix = matrix.sort_values("script", axis=1, ascending=False)
matrix = matrix.reindex(matrix.mean().sort_values(ascending=False).index, axis=1)

print(analyze.cosine_similarity_row(matrix, "script", "good"))
print(analyze.cosine_similarity_row(matrix, "script", "bad"))
print(analyze.cosine_similarity_row(matrix, "bad", "good"))
# %%
