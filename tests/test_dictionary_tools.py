from docsim.library import dictionary_tools


nested_dictionary = {1: {"col": "This is a test."}, 2: {"col": "This is also a test."}}
test_dictionary_with_int_keys = {"1": "test", "2": "value"}


def test_fold_nested_dictionary():
    result = dictionary_tools.fold_nested_dictionary(nested_dictionary, "col")
    assert result[1] == "This is a test."


def test_replace_string_value_as_list():
    result = dictionary_tools.replace_string_value_as_list(
        test_dictionary_with_int_keys
    )
    assert result["1"] == ["test"]


def test_replace_string_key():
    result = dictionary_tools.replace_string_key(
        test_dictionary_with_int_keys, "2", "3"
    )
    assert result["3"] == "value"


def test_string_key_as_int():
    result = dictionary_tools.string_key_as_int(test_dictionary_with_int_keys)
    assert result[1] == "test"
