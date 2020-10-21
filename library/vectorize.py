from sklearn.feature_extraction.text import CountVectorizer

def create_doc_term_matrix(docs: list):
docs = list(df.text)
vec = CountVectorizer()
X = vec.fit_transform(docs)
matrix = pd.DataFrame(
    X.toarray(), columns=vec.get_feature_names(), index=df.index)
print('Number of words with no preprocessing: ', len(matrix.columns))
matrix.sample()

