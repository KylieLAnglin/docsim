# %%

import nltk

from nltk.book import *

from nltk.corpus import wordnet

# %%
text6.concordance


# %%
corpus_loc = "/Users/kylie/Dropbox/Active/docsim/data/plain text transcripts"

docs = nltk.corpus.PlaintextCorpusReader(corpus_loc, ".*\.txt")
print(docs.fileids())

docs_processed = nltk.Text(docs.words())

docs_processed.concordance("ethan")

# %%

wordnet.synsets("behavior")

wordnet.synset("behavior.n.01").lemma_names()

wordnet.synsets("misbehavior")

wordnet.synset("misbehavior.n.01").lemma_names()

wordnet.synsets("misbehaves")
wordnet.synset("misbehaves.v.01").lemma_names()


for synset in wordnet.synsets("equity", wordnet.NOUN):
    print(synset.name() + ":", synset.definition())

wordnet.synsets("equity")[4].lemma_names()

# %%
