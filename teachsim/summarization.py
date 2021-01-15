import spacy
import pytextrank


transcript_df = pd.read_csv(start.CLEAN_FILEPATH + "text_transcripts.csv")
transcript_df["id"] = transcript_df.id.astype(str)
transcript_df = transcript_df.set_index(["study", "id"])

fix_spaces = lambda x: " ".join(x.split())
get_text = lambda dataframe: " ".join(dataframe["clean_text"].apply(fix_spaces).values)


text_df = transcript_df.merge(df, left_index=True, right_index=True)
text_df["cluster"] = np.where(text_df["pca2"] > 0.1, "one", "two")
restricted_text_df = text_df.loc[text_df["pca1"] < 0.1]

# example text
text = get_text(restricted_text_df[restricted_text_df["cluster"] == "one"])

# load a spaCy model, depending on language, scale, etc.
nlp = spacy.load("en_core_web_sm")

# add PyTextRank to the spaCy pipeline
tr = pytextrank.TextRank()
nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)

doc = nlp(text)

# examine the top-ranked phrases in the document
for p in doc._.phrases:
    print("{:.4f} {:5d}  {}".format(p.rank, p.count, p.text))
    print(p.chunks)


for sent in doc._.textrank.summary(limit_phrases=15, limit_sentences=5):
    print(sent)

text = get_text(restricted_text_df[restricted_text_df["cluster"] == "two"])

# load a spaCy model, depending on language, scale, etc.
nlp = spacy.load("en_core_web_sm")

# add PyTextRank to the spaCy pipeline
tr = pytextrank.TextRank()
nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)

doc = nlp(text)

# examine the top-ranked phrases in the document
for p in doc._.phrases:
    print("{:.4f} {:5d}  {}".format(p.rank, p.count, p.text))
    print(p.chunks)


for sent in doc._.textrank.summary(limit_phrases=15, limit_sentences=5):
    print(sent)
