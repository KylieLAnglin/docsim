import os
import fnmatch

import docx


def import_text(filepath: str, pattern: str):
    """Searches folder for docx files and extracts text

    Args:
        filepath (str): filepath to folder containing docx files
        pattern (str): search pattern

    Returns:
        [dict]: dictionary of filenames and text
    """
    doc_dict = {}
    for filename in os.listdir(filepath):
        if fnmatch.fnmatch(filename, pattern):
            docfile = filepath + filename
            print(filename)
            doc = docx.Document(docfile)
            text_list = []
            for para in doc.paragraphs:
                text_list.append(para.text)
            text = " ".join(text_list)
    doc_dict[filename] = text

    return doc_dict