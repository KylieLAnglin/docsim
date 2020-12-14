import pytest

from docsim.library import clean_text
from docsim.library import start


def test_import_text():
    test = clean_text.import_text(
        filepath=start.code_dir + "tests/test_data/", pattern="*docx"
    )
    assert len((test)) == 2
