
# coding: utf-8

# # Create Document-Term Matrices
# * No pre-processing
# * Remove stop words
# * Remove stop words + tf-idf
# * Stem
# * Stem + Stop Words
# * Stem + Stop + Tf-IDF

# ## Create full df

# In[30]:


import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy

nlp = spacy.load('en', disable=['parser', 'ner'])


dir = '/Users/kylie/docsim/'

clean_filepath = dir + "data/clean/"


# In[3]:


df_corpus = pd.read_csv(clean_filepath + 'text_transcripts.csv')
df_corpus = df_corpus.set_index('doc')
df_corpus.sample(5)


# In[4]:


df_ideal = pd.read_csv(clean_filepath + 'text_scripts.csv')
df_ideal = df_ideal.set_index('doc')
df_ideal.sample(3)


# In[5]:


df = df_ideal.append(df_corpus, sort=True)
df.sample(5)


df[df.text.isnull()]


# # Simple Doc-Term Matrix


docs = list(df.text)
vec = CountVectorizer()
X = vec.fit_transform(docs)
matrix = pd.DataFrame(
    X.toarray(), columns=vec.get_feature_names(), index=df.index)
print('Number of words with no preprocessing: ', len(matrix.columns))
matrix.sample()

matrix_ideal = matrix[matrix.index.str.contains('Model')]
matrix_ideal.to_csv(clean_filepath + 'matrix_scripts.csv')
matrix_ideal.sample(5)

matrix_corpus = matrix[~matrix.index.str.contains('Model')]
matrix_corpus.to_csv(clean_filepath + 'matrix_transcripts.csv')
matrix_corpus.sample()


# # Weight

# In[10]:


docs = list(df.text)
vec = TfidfVectorizer()
X = vec.fit_transform(docs)
matrix_wgt = pd.DataFrame(
    X.toarray(), columns=vec.get_feature_names(), index=df.index)
matrix_wgt.sample()

matrix_ideal_wgt = matrix_wgt[matrix_wgt.index.str.contains('Model')]
matrix_ideal_wgt.to_csv(clean_filepath + 'matrix_scripts_wgt.csv')
matrix_ideal_wgt.sample()


matrix_corpus_wgt = matrix_wgt[~matrix_wgt.index.str.contains('Model')]
matrix_corpus_wgt.to_csv(clean_filepath + 'matrix_transcripts_wgt.csv')
matrix_corpus_wgt.sample()


# # Remove Stop Words (no weighting)

# In[11]:


stop_words = list(stopwords.words('english'))
stop_words.append('like')
stop_words.append('um')
stop_words.append('uhm')
stop_words.append('-pron-')
stop_words.append('pron')
stop_words.append('yeah')
stop_words.append('okay')

stop_words


docs = list(df.text)
vec = CountVectorizer(stop_words=stop_words)
X = vec.fit_transform(docs)
matrix_stop = pd.DataFrame(
    X.toarray(), columns=vec.get_feature_names(), index=df.index)
print('Number of words after removing stop words: ', len(matrix_stop.columns))
matrix_stop.sample()


matrix_ideal_stop = matrix_stop[matrix_stop.index.str.contains('Model')]
matrix_ideal_stop.to_csv(clean_filepath + 'matrix_scripts_stop.csv')
matrix_ideal_stop.sample()


matrix_corpus_stop = matrix_stop[~matrix_stop.index.str.contains('Model')]
matrix_corpus_stop.to_csv(clean_filepath + 'matrix_transcripts_stop.csv')
matrix_corpus_stop.sample()


# # Stop and weight

# In[15]:


docs = list(df.text)
vec = TfidfVectorizer(stop_words=stop_words)
X = vec.fit_transform(docs)
matrix_stop_wgt = pd.DataFrame(
    X.toarray(), columns=vec.get_feature_names(), index=df.index)
print('Number of words: ', len(matrix_stop_wgt.columns))
matrix_stop_wgt.sample()

matrix_ideal_stop_wgt = matrix_stop_wgt[matrix_stop_wgt.index.str.contains(
    'Model')]
matrix_ideal_stop_wgt.to_csv(clean_filepath + 'matrix_scripts_stop_wgt.csv')
matrix_ideal_stop_wgt.sample()


matrix_corpus_stop_wgt = matrix_stop_wgt[~matrix_stop_wgt.index.str.contains(
    'Model')]
matrix_corpus_stop_wgt.to_csv(
    clean_filepath + 'matrix_transcripts_stop_wgt.csv')
matrix_corpus_stop_wgt.sample()


# %% Stem


nlp = spacy.load('en', disable=['parser', 'ner'])

sentence = "The striped bats are hanging on their feet for best singing."

# Parse the sentence using the loaded 'en' model object `nlp`
doc = nlp(sentence)

# Extract the lemma for each token and join
" ".join([token.lemma_ for token in doc])
# > 'the strip bat be hang on -PRON- foot for good'


stems = [" ".join([token.lemma_ for token in nlp(text)]) for text in df.text]
df['text'] = stems
df.sample(5)


docs = list(df.text)
vec = CountVectorizer()
X = vec.fit_transform(docs)
matrix_stem = pd.DataFrame(
    X.toarray(), columns=vec.get_feature_names(), index=df.index)
print('Number of words after stemming: ', len(matrix_stem.columns))
matrix_stem.sample()


matrix_scripts_stem = matrix_stem[matrix_stem.index.str.contains('Model')]
matrix_scripts_stem.to_csv(clean_filepath + 'matrix_scripts_stem.csv')
matrix_scripts_stem.sample()


matrix_transcripts_stem = matrix_stem[~matrix_stem.index.str.contains('Model')]
matrix_transcripts_stem.to_csv(clean_filepath + 'matrix_transcripts_stem.csv')
matrix_transcripts_stem.sample()


# # Stop and Stem

# In[21]:


docs = list(df.text)
vec = CountVectorizer(stop_words=stop_words)
X = vec.fit_transform(docs)
matrix_stem_stop = pd.DataFrame(
    X.toarray(), columns=vec.get_feature_names(), index=df.index)
print('Number of words: ', len(matrix_stem_stop.columns))
matrix_stem_stop.sample()

matrix_scripts_stem_stop = matrix_stem_stop[matrix_stem_stop.index.str.contains(
    'Model')]
matrix_scripts_stem_stop.to_csv(
    clean_filepath + 'matrix_scripts_stem_stop.csv')
matrix_scripts_stem_stop.sample()

matrix_transcripts_stem_stop = matrix_stem_stop[~matrix_stem_stop.index.str.contains(
    'Model')]
matrix_transcripts_stem_stop.to_csv(
    clean_filepath + 'matrix_transcripts_stem_stop.csv')
matrix_transcripts_stem_stop.sample()


# # Stop Stem and Weight

# In[24]:


docs = list(df.text)
vec = TfidfVectorizer(stop_words=stop_words)
X = vec.fit_transform(docs)
matrix_stem_stop_wgt = pd.DataFrame(
    X.toarray(), columns=vec.get_feature_names(), index=df.index)
print('Number of words after stopping and stemming: ', len(matrix_stem_stop_wgt.columns))
matrix_stem_stop_wgt.sample()


matrix_scripts_stem_stop_wgt = matrix_stem_stop_wgt[matrix_stem_stop_wgt.index.str.contains(
    'Model')]
matrix_scripts_stem_stop_wgt.to_csv(
    clean_filepath + 'matrix_scripts_stem_stop_wgt.csv')
matrix_scripts_stem_stop_wgt.sample()


matrix_transcripts_stem_stop_wgt = matrix_stem_stop_wgt[~matrix_stem_stop_wgt.index.str.contains(
    'Model')]
matrix_transcripts_stem_stop_wgt.to_csv(
    clean_filepath + 'matrix_transcripts_stem_stop_wgt.csv')
matrix_transcripts_stem_stop_wgt.sample()


# # LSA

# In[43]:


matrix_transcripts_lsa = pd.read_csv(clean_filepath + 'matrix_transcripts.csv')
matrix_scripts_lsa = pd.read_csv(clean_filepath + 'matrix_scripts.csv')
matrix_lsa = matrix_transcripts_lsa.append(matrix_scripts_lsa)
matrix_lsa = matrix_lsa.set_index('doc')

lsa = TruncatedSVD(n_components=100, random_state=100)
lsa_fit = lsa.fit_transform(matrix_lsa)
lsa_fit = Normalizer(copy=False).fit_transform(lsa_fit)
print(lsa_fit.shape)

#  Each LSA component is a linear combo of words
word_weights = pd.DataFrame(lsa.components_, columns=matrix_lsa.columns)
word_weights.head()
word_weights_trans = word_weights.T

# Each document is a linear combination of components
matrix_lsa = pd.DataFrame(
    lsa_fit, index=matrix_lsa.index, columns=word_weights.index)
matrix_lsa.sample(5)


matrix_scripts_lsa = matrix_lsa[matrix_lsa.index.str.contains('Model')]
matrix_scripts_lsa.to_csv(clean_filepath + 'matrix_scripts_lsa.csv')

matrix_transcripts_lsa = matrix_lsa[~matrix_lsa.index.str.contains('Model')]
matrix_transcripts_lsa.to_csv(clean_filepath + 'matrix_transcripts_lsa.csv')

word_weights_trans.to_csv(clean_filepath + 'lsa_topics.csv')

print('Number of words after lsa: ', len(matrix_transcripts_lsa.columns))


# # LSA + Stop

# In[43]:

matrix_transcripts_lsa_stop = pd.read_csv(
    clean_filepath + 'matrix_transcripts_stop.csv')
matrix_scripts_lsa_stop = pd.read_csv(
    clean_filepath + 'matrix_scripts_stop.csv')
matrix_lsa_stop = matrix_transcripts_lsa_stop.append(matrix_scripts_lsa_stop)
matrix_lsa_stop = matrix_lsa_stop.set_index('doc')

lsa = TruncatedSVD(n_components=100, random_state=100)
lsa_fit = lsa.fit_transform(matrix_lsa_stop)
lsa_fit = Normalizer(copy=False).fit_transform(lsa_fit)
print(lsa_fit.shape)

# Each LSA component is a linear combo of words
word_weights = pd.DataFrame(lsa.components_, columns=matrix_lsa_stop.columns)
word_weights.head()
word_weights_trans = word_weights.T

# Each document is a linear combination of components
matrix_lsa_stop = pd.DataFrame(
    lsa_fit, index=matrix_lsa.index, columns=word_weights.index)
matrix_lsa_stop.sample(5)


matrix_scripts_lsa_stop = matrix_lsa_stop[matrix_lsa_stop.index.str.contains(
    'Model')]
matrix_scripts_lsa_stop.to_csv(clean_filepath + 'matrix_scripts_lsa_stop.csv')

matrix_transcripts_lsa_stop = matrix_lsa_stop[~matrix_lsa_stop.index.str.contains(
    'Model')]
matrix_transcripts_lsa_stop.to_csv(
    clean_filepath + 'matrix_transcripts_lsa_stop.csv')

word_weights_trans.to_csv(clean_filepath + 'lsa_stop_topics.csv')


# # LSA + Weights

# In[44]:


matrix_transcripts_lsa_wgt = pd.read_csv(
    clean_filepath + 'matrix_transcripts_wgt.csv')
matrix_scripts_lsa_wgt = pd.read_csv(clean_filepath + 'matrix_scripts_wgt.csv')
matrix_lsa_wgt = matrix_transcripts_lsa_wgt.append(matrix_scripts_lsa_wgt)
matrix_lsa_wgt = matrix_lsa_wgt.set_index('doc')

lsa = TruncatedSVD(n_components=100, random_state=100)
lsa_fit = lsa.fit_transform(matrix_lsa_wgt)
lsa_fit = Normalizer(copy=False).fit_transform(lsa_fit)
print(lsa_fit.shape)

# Each LSA component is a linear combo of words
word_weights = pd.DataFrame(lsa.components_, columns=matrix_lsa_wgt.columns)
word_weights.head()
word_weights_trans = word_weights.T


# Each document is a linear combination of components
matrix_lsa_wgt = pd.DataFrame(
    lsa_fit, index=matrix_lsa_wgt.index, columns=word_weights.index)
matrix_lsa_wgt.sample(5)


matrix_scripts_lsa_wgt = matrix_lsa_wgt[matrix_lsa_wgt.index.str.contains(
    'Model')]
matrix_scripts_lsa_wgt.to_csv(clean_filepath + 'matrix_scripts_lsa_wgt.csv')

matrix_transcripts_lsa_wgt = matrix_lsa_wgt[~matrix_lsa_wgt.index.str.contains(
    'Model')]
matrix_transcripts_lsa_wgt.to_csv(
    clean_filepath + 'matrix_transcripts_lsa_wgt.csv')

word_weights_trans.to_csv(clean_filepath + 'lsa_wgt_topics.csv')


# LSA, Weighting, Stop Words

# In[45]:


matrix_transcripts_lsa_wgt_stop = pd.read_csv(
    clean_filepath + 'matrix_transcripts_stop_wgt.csv')
matrix_scripts_lsa_wgt_stop = pd.read_csv(
    clean_filepath + 'matrix_scripts_stop_wgt.csv')
matrix_lsa_wgt_stop = matrix_transcripts_lsa_wgt_stop.append(
    matrix_scripts_lsa_wgt_stop)
matrix_lsa_wgt_stop = matrix_lsa_wgt_stop.set_index('doc')

lsa = TruncatedSVD(n_components=100, random_state=100)
lsa_fit = lsa.fit_transform(matrix_lsa_wgt_stop)
lsa_fit = Normalizer(copy=False).fit_transform(lsa_fit)
print(lsa_fit.shape)

# Each LSA component is a linear combo of words
word_weights = pd.DataFrame(
    lsa.components_, columns=matrix_lsa_wgt_stop.columns)
word_weights.head()
word_weights_trans = word_weights.T


# Each document is a linear combination of components
matrix_lsa_wgt_stop = pd.DataFrame(
    lsa_fit, index=matrix_lsa_wgt_stop.index, columns=word_weights.index)
matrix_lsa_wgt_stop.sample(5)


matrix_scripts_lsa_wgt_stop = matrix_lsa_wgt_stop[matrix_lsa_wgt_stop.index.str.contains(
    'Model')]
matrix_scripts_lsa_wgt_stop.to_csv(
    clean_filepath + 'matrix_scripts_lsa_wgt_stop.csv')

matrix_transcripts_lsa_wgt_stop = matrix_lsa_wgt_stop[~matrix_lsa_wgt_stop.index.str.contains(
    'Model')]
matrix_transcripts_lsa_wgt_stop.to_csv(
    clean_filepath + 'matrix_transcripts_lsa_wgt_stop.csv')

word_weights_trans.to_csv(clean_filepath + 'lsa_wgt_stop_topics.csv')
