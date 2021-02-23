import nltk
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
import nltk

nltk.download("punkt")
stop_words = set(nltk.corpus.stopwords.words("english"))
lemma = nltk.wordnet.WordNetLemmatizer()


ps = PorterStemmer()


def process_text(
    text: str,
    lower_case: bool = True,
    remove_punct: bool = True,
    remove_stopwords: bool = False,
    lemma: bool = False,
):

    tokens = nltk.word_tokenize(text)

    if lower_case:
        tokens = [token.lower() if token.isalpha() else token for token in tokens]

    if remove_punct:
        tokens = [token for token in tokens if token.isalpha()]

    if remove_stopwords:
        tokens = [token for token in tokens if not token in stop_words]

    if lemma:
        tokens = [nltk.wordnet.WordNetLemmatizer().lemmatize(token) for token in tokens]

    # if lemma:  # lemma needs to go first because spacy lemmatizer depends on context
    #     doc = " ".join([ps.stem(token)])

    # elif not lemma:
    #     doc = " ".join([token.text for token in nlp(text)])

    doc = " ".join(tokens)
    return doc


# %%


# %%


def vectorize_text(
    df: pd.DataFrame,
    text_col: str,
    remove_stopwords: bool = False,
    tfidf: bool = False,
    lemma: bool = False,
    lsa: bool = False,
    n_components: int = 100,
    n_gram_range=(1, 1),
):

    docs = [
        process_text(
            text,
            lower_case=True,
            remove_punct=False,
            remove_stopwords=remove_stopwords,
            lemma=lemma,
        )
        for text in df[text_col]
    ]

    if tfidf == False:
        vec = CountVectorizer(ngram_range=n_gram_range)

    elif tfidf:
        vec = TfidfVectorizer(ngram_range=n_gram_range)

    X = vec.fit_transform(docs)
    matrix = pd.DataFrame(X.toarray(), columns=vec.get_feature_names(), index=df.index)

    print("Number of words: ", len(matrix.columns))

    if lsa:
        lsa_dfs = create_lsa_dfs(matrix=matrix, n_components=n_components)
        matrix = lsa_dfs.matrix
        print("Number of dimensions: ", len(matrix.columns))

    return matrix