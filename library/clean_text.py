import os
import fnmatch
import re
import spacy

nlp = spacy.load("en_core_web_lg", disable=["parser", "ner"])


import docx

from docsim.library import dictionary_tools


def import_text(filepath: str, pattern: str, paragraph_tag: str = None):
    """Searches folder for docx files and extracts text

    Args:
        filepath (str): filepath to folder containing docx files
        pattern (str): search pattern

    Returns:
        [dict]: dictionary of filenames and text
    """
    doc_dict = {}
    for filename in os.listdir(filepath):
        if fnmatch.fnmatch(filename, pattern) and not filename.startswith("~$"):
            print(filename)
            docfile = filepath + filename
            doc = docx.Document(docfile)
            text_list = []
            for para in doc.paragraphs:
                if paragraph_tag is None:
                    text_list.append(para.text)
                elif paragraph_tag and (len(para.text) > 0):
                    segmented_text = paragraph_tag + para.text
                    text_list.append(segmented_text)
            text = " ".join(text_list)
            doc_dict[filename] = text

    return doc_dict


def filter_segments(
    text: str, segment_tag: str, filter_tag: str, keep_if_tagged: bool = True
):
    """Filters a text by searching individual segments for instance of string

    Args:
        text (str): string to filter
        segment_tag (str): tag indicating text segments to search
        filter_tag (str): string to search for
        keep_if_tagged (bool, optional): Keep segment if contains filter_tag? Defaults to True.

    Returns:
        [str]: filtered string
    """
    segments = [
        segment_tag + " " + string.strip()
        for string in text.split(segment_tag)
        if string
    ]
    filtered_segments = [segment for segment in segments if filter_tag in segment]
    filtered_text = " ".join(filtered_segments)

    return filtered_text


def add_whitespace_after_punct(s):
    return re.sub(r"([.?!])", ". ", re.sub(r" +", " ", s))


def remove_trailing_hyphen(s):
    return re.sub(r"(-+)\s", " ", re.sub(r" +", " ", s))


def remove_leading_hyphen(s):
    return re.sub(r"\s(-+)", " ", re.sub(r" +", " ", s))


def remove_hyphens(s):
    return s.replace("-", " ")


def word_family_from_dict(text: str, families: dict):
    """Replace words found in dictionary values (list) with key

    Args:
        text (str): String with substrings to replace
        families (dict): Word family name in key, list of members as value

    Returns:
        new_text: String with word family members replaced with word family name
    """
    new_dict = dictionary_tools.long_inverse_dict_from_key_list(families)
    doc = nlp(text)
    old_words = list(new_dict.keys())

    new_text = ""
    for token in doc:
        token = str(token.text)
        if token in old_words:
            token = token.replace(token, new_dict[token])

        new_text = new_text + token + " "

    # for word in new_dict:
    #     new_text = new_text.replace(word, new_dict[word])

    return new_text
