from sklearn.feature_extraction.text import CountVectorizer


def create_doc_term_matrix(docs: list):
    docs = list(df.text)
    vec = CountVectorizer()
    X = vec.fit_transform(docs)
    matrix = pd.DataFrame(X.toarray(), columns=vec.get_feature_names(), index=df.index)
    print("Number of words with no preprocessing: ", len(matrix.columns))
    matrix.sample()


def vectorize_text(
    df: pd.DataFrame,
    text_col: str,
    remove_stopwords: bool = False,
    tfidf: bool = False,
    lemma: bool = False,
    lsa: bool = False,
):
    docs = list(df[text_col])
    if remove_stopwords == False:
        stop_words = []

    elif remove_stopwords:
        stop_words = list(stopwords.words("english"))

    if lemma:
        docs = [
            " ".join([token.lemma_ for token in nlp(text)]) for text in df[text_col]
        ]

    if tfidf == False:
        vec = CountVectorizer(stop_words=stop_words)

    elif tfidf:
        vec = TfidfVectorizer(stop_words=stop_words)

    X = vec.fit_transform(docs)
    matrix = pd.DataFrame(X.toarray(), columns=vec.get_feature_names(), index=df.index)

    print("Number of words: ", len(matrix.columns))

    if lsa:
        lsa_dfs = create_lsa_dfs(matrix=matrix)
        matrix = lsa_dfs.matrix
        print("Number of dimensions: ", len(matrix.columns))

    return matrix