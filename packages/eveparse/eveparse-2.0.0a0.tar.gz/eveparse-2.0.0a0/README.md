# Eve Parse

Parser for Eve Online - extract type ids, quantities, and errors from a text string

## Install

```shell
pip install eveparse
```

## Usage

The `parse()` function takes a text string and returns a dict of items and errors.

```python
import eveparse

string = "Ragnarok	1"
results = eveparse.parse(string)
print(results)  # {'items': {'23773': 1}, 'errors': []}
```

## Test

```shell
python -m unittest
```
