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


def test_filter_segments():
    test = "[New Speaker] Interviewer: This is string. [New Speaker] And this is a second string."
    result = clean_text.filter_segments(
        test, segment_tag="[New Speaker]", filter_tag="Interviewer:"
    )

    assert result == "[New Speaker] Interviewer: This is string."
