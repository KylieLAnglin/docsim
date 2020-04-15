doc_words = {}
for doc in doc_text:
    doc_words[doc] = word_tokenize(doc_text[doc])