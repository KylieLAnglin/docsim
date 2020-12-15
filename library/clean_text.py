import os
import fnmatch
import re

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
