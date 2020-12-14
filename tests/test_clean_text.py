import pytest

from docsim.library import clean_text
from docsim.library import start


def test_import_text():
    test = clean_text.import_text(
        filepath=start.code_dir + "tests/test_data/", pattern="*docx"
    )
    assert len((test)) == 2


def test_import_text_segmented():
    test = clean_text.import_text(
        filepath=start.code_dir + "tests/test_data/",
        pattern="*docx",
        paragraph_tag="[New Speaker]",
    )

    print(test)
    assert test["test1.docx"].count("[New Speaker]") == 2


def test_replace_substring_in_dict():
    test_dict = {
        "test1": "Interviewer: This is a text.",
        "test2": "Interviewee: This is a text.",
    }

    test = clean_text.replace_substring_in_dict(
        test_dict, "Interviewer:", "Interviewee:"
    )
    assert test["test1"] == "Interviewee: This is a text."
