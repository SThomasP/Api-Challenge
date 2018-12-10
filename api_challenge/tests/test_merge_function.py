from api_challenge import merge_dicts


# test that two dicts with none of the same keys will merge as expected
def test_merge_strings_only_no_overwrite():
    merge_from = {'a': 'a', 'b': 'b'}
    merge_into = {'c': 'c', 'd': 'd'}
    result = merge_dicts(merge_from, merge_into)
    assert {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd'} == result


# test that two dicts with some of the same keys will merge as expected
def test_merge_strings_only_with_overwrite():
    merge_from = {'a': 'a', 'b': 'bb', 'c': 'c'}
    merge_into = {'a': 'aa', 'b': 'b', 'd': 'd'}
    result = merge_dicts(merge_from, merge_into)
    assert {'a': 'a', 'b': 'bb', 'c': 'c', 'd': 'd'} == result


# test that two dicts will merge recursively as expected
def test_merge_recursive_no_overwrite():
    merge_from = {'a': {'aa': 'aa', 'ab': 'ab'}, 'b': 'b'}
    merge_into = {'a': {'ac': 'ac'}, 'c': 'c'}
    result = merge_dicts(merge_from, merge_into)
    assert {'a': {'aa': 'aa', 'ab': 'ab', 'ac': 'ac'}, 'b': 'b', 'c': 'c'} == result


# test that two dicts will merge recursively when they have the same keys
def test_merge_recursive_with_overwrite():
    merge_from = {'a': {'aa': 'aa', 'ab': 'ab'}, 'b': 'b'}
    merge_into = {'a': {'ab': 'ac'}, 'b': 'bc'}
    result = merge_dicts(merge_from, merge_into)
    assert {'a': {'aa': 'aa', 'ab': 'ab'}, 'b': 'b'} == result


# test that a dict will be overwritten when the next dict has the same key
def test_merge_overwrite_dict():
    merge_from = {'a': {'ab': 'ab', 'ac': 'ac'}}
    merge_into = {'a': {'ab': {'aba': 'aba'}}}
    result = merge_dicts(merge_from, merge_into)
    assert {'a': {'ab': 'ab', 'ac': 'ac'}} == result


# test that a list will be extended when another list is merged into it.
def test_merge_list_extend():
    merge_from = {'a': [0, 1, 2]}
    merge_into = {'a': [1, 2, 1]}
    result = merge_dicts(merge_from, merge_into)
    assert {'a': [1, 2, 1, 0, 1, 2]} == result

