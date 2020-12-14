import os
import fnmatch

import docx


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
        if fnmatch.fnmatch(filename, pattern):
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


def replace_substring_in_dict(string_dict: dict, old_str: str, new_str: str):
    """Replaces substrings within dict values

    Args:
        dict (dict): dictionary with string values
        old_str (str): old substring
        new_str (str): new substring

    Returns:
        [dict]: same dictionary with new values
    """
    new_dict = string_dict.copy()

    for key in new_dict.keys():
        new_dict[key] = new_dict[key].replace(old_str, new_str)

    return new_dict
