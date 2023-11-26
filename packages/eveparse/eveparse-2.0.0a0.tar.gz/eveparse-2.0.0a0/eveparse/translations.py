import json
import pathlib

BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH / "data"
MARKET_GROUPS_PATH = DATA_PATH / "market_groups.json"
META_PATH = DATA_PATH / "meta_groups.json"
TYPE_PATH = DATA_PATH / "types.json"

with MARKET_GROUPS_PATH.open("r") as file:
    market_groups_data = json.load(file)
    MARKET_GROUPS = set(market_groups_data)

with META_PATH.open("r") as file:
    meta_groups_data = json.load(file)
    META_GROUPS = set(meta_groups_data)

with TYPE_PATH.open("r") as file:
    TYPE_DICT = json.load(file)
    TYPE_NAMES = set(TYPE_DICT.keys())

ISK_UNITS = ['isk', '星币']
VOLUME_UNITS = ['m3', 'm³', 'м^3']
DROP_DESTROY = [
    'destroyed',
    'dropped',
    '击杀',
    '掉落',
    'largué',
    'détruit',
    'zerstört',
    'fallengelassen',
    '破壊された',
    'ドロップした',
    '파괴됨',
    '드랍됨',
    'выпало в трофеи',
    'уничтожено',
    'soltado',
    'destruido',
]
