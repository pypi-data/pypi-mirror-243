from .. import converters
from .. import errors

reprocessed_item_partitions = [
    (" (", " Units)"),
    (" (", "个单位)"),
    (" (", " unités)"),
    (" (", " Einheiten)"),
    ("（", " ユニット）"),
    (" (", " 유닛)"),
    (" (", " единиц)"),
    (" (", " unidades)"),
]


def industry_reprocessed_materials(string: str) -> dict:
    """Tritanium (385 Units)"""

    for separator, ending in reprocessed_item_partitions:
        if separator in string and string.endswith(ending):
            trimmed_string = string.rstrip(ending)
            type_name, quantity_string = trimmed_string.split(sep=separator)
            type_id = converters.type_name_to_type_id(string=type_name)
            quantity = converters.quantity_to_int(string=quantity_string)
            return {type_id: quantity}
    else:
        raise errors.ParserError


def industry_required_for(string: str) -> dict:
    return {}


def variations(string: str) -> dict:
    return {}


def variations_compare(string: str) -> dict:
    return {}


if __name__ == '__main__':
    s = """
    Tritanium (385 Units)
    Isogen (20 Units)
    Nocxium (65 Units)
    Megacyte (10 Units)
    Robotics (25 Units)
    Morphite (15 Units)
    Photon Microprocessor (5 Units)
    Laser Focusing Crystals (5 Units)

    三钛合金* (30710个单位)
    类晶体胶矿* (17250个单位)
    类银超金属* (4921个单位)
    同位聚合体* (1527个单位)
    超新星诺克石* (597个单位)
    晶状石英核岩* (300个单位)
    超噬矿* (512个单位)

    Tritanium* (834277 unités)
    Pyérite* (611423 unités)
    Mexallon* (116778 unités)
    Isogène* (72656 unités)
    Nocxium* (12230 unités)
    Zydrine* (4977 unités)
    Mégacyte* (6341 unités)

    Tritanium* (834277 Einheiten)
    Pyerite* (611423 Einheiten)
    Mexallon* (116778 Einheiten)
    Isogen* (72656 Einheiten)
    Nocxium* (12230 Einheiten)
    Zydrine* (4977 Einheiten)
    Megacyte* (6341 Einheiten)

    トリタニウム*（3826117 ユニット）
    パイライト*（828100 ユニット）
    メクサロン*（342157 ユニット）
    アイソゲン*（56183 ユニット）
    ノキシウム*（16433 ユニット）
    ザイドリン*（5466 ユニット）
    メガサイト*（2500 ユニット）

    트리타늄* (834277 유닛)
    파이어라이트* (611423 유닛)
    멕살론* (116778 유닛)
    이소젠* (72656 유닛)
    녹시움* (12230 유닛)
    자이드라인* (4977 유닛)
    메가사이트* (6341 유닛)

    Tritanium* (834277 единиц)
    Pyerite* (611423 единицы)
    Mexallon* (116778 единиц)
    Isogen* (72656 единиц)
    Nocxium* (12230 единиц)
    Zydrine* (4977 единиц)
    Megacyte* (6341 единица)

    Tritanio* (834277 unidades)
    Pierita* (611423 unidades)
    Mexalón* (116778 unidades)
    Isogen* (72656 unidades)
    Nocxium* (12230 unidades)
    Zidrina* (4977 unidades)
    Megacita* (6341 unidades)
    """
    for line in s.splitlines():
        items = industry_reprocessed_materials(line)
        print(items)
