from eveparse import parse


def test_empty_text():
    text = " "
    result = parse(text)
    assert result == {"items": {}, "errors": []}


def test_single_line():
    text = "Rifter\t1"
    result = parse(text)
    assert result == {"items": {587: 1}, "errors": []}


def test_multi_line():
    text = """Rifter\t1
    Rifter\t1"""
    result = parse(text)
    assert result == {"items": {587: 2}, "errors": []}


def test_multi_line_empty():
    text = """Rifter\t1

    Rifter\t1"""
    result = parse(text)
    assert result == {"items": {587: 2}, "errors": []}


def test_multi_line_error():
    text = """Rifter\t1
    Rifte\t1"""
    result = parse(text)
    assert result == {"items": {587: 1}, "errors": ['    Rifte\t1']}
