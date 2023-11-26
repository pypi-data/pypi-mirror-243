import re

# TODO: handle other character encodings
# TODO: support 2x item_name
# TODO: support Evepraisal/Janice URLs
# TODO: aggregate quantities of same name
# TODO: support orbital platform window - 	36200	Water Tier 1
# tornado x2 - supported
# 2x tornado - unsupported

META_LEVELS = [
    "Tech I",
    "Tech II",
    "Tech III",
    "Storyline",
    "Deadspace",
    "Faction",
    "Officer",
]

QUANTITY_NAME = re.compile(r"[\d+\.,]+\s+\S+", re.IGNORECASE)
NAME_QUANTITY = re.compile(r".+\s+[\d+\.,]+$", re.IGNORECASE)


def parse(text):
    items = []
    errors = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            name, quantity = parse_line(line)
        except Exception as e:
            errors.append(line)
        else:
            name = name.strip("*").strip().lower()
            items.append({"name": name, "quantity": quantity})
    return items, errors


def parse_line(line):
    strings = line.split("\t")
    if len(strings) == 1:
        return parse_1(strings[0])

    # Compare window may have many columns,
    # but will have meta levels in column 2
    elif strings[1] in META_LEVELS:
        return strings[0], 1

    elif len(strings) == 2:
        return parse_2(strings)
    elif len(strings) == 3:
        return parse_3(strings)
    elif len(strings) == 4:
        return parse_4(strings)
    elif len(strings) == 5:
        return parse_5(strings)
    elif len(strings) == 7:
        return parse_7(strings)
    else:
        raise NotImplementedError(len(strings))


def parse_1(string):
    if string == "Components" or string == "Items":
        raise ValueError()
    if string.startswith("["):
        string = string.strip("[")
        name, _ = string.split(", ")
        return name, 1
    elif " x " in string:
        _quantity, name = string.split(" x ")
        digital, quantity = is_digit(_quantity)
        if digital:
            return name, quantity
    elif " x" in string:
        name, _quantity = string.split(" x")
        digital, quantity = is_digit(_quantity)
        if digital:
            return name, quantity
    elif QUANTITY_NAME.match(string):
        parts = string.split()
        _quantity = parts[0]
        name = " ".join(parts[1:])
        digital, quantity = is_digit(_quantity)
        if digital:
            return name, quantity
    elif NAME_QUANTITY.match(string):
        parts = string.split()
        _quantity = parts[-1]
        name = " ".join(parts[:-1])
        digital, quantity = is_digit(_quantity)
        if digital:
            return name, quantity
    return string, 1


def parse_2(strings):
    name, _quantity = strings
    digital, quantity = is_digit(_quantity)
    if digital:
        return name, quantity
    raise ValueError()


def parse_3(strings):
    name, _quantity, _ = strings
    digital, quantity = is_digit(_quantity)
    if digital:
        return name, quantity
    raise ValueError()


def parse_4(strings):
    if strings[0] == "Total:":
        raise ValueError()

    name, _quantity, *_ = strings
    digital, quantity = is_digit(_quantity)
    if digital:
        return name, quantity

    name, _, _quantity, _ = strings
    digital, quantity = is_digit(_quantity)
    if digital:
        return name, quantity

    name, *_, _quantity = strings
    digital, quantity = is_digit(_quantity)
    if digital:
        return name, quantity
    raise ValueError()


def parse_5(strings):
    if strings == ["Item", "Required", "Available", "Est. Unit price", "typeID"]:
        raise ValueError()
    name, _quantity, *_ = strings
    digital, quantity = is_digit(_quantity)
    if digital:
        return name, quantity
    raise ValueError()


def parse_7(strings):
    name, _quantity, *_ = strings
    digital, quantity = is_digit(_quantity)
    if digital:
        return name, quantity
    raise ValueError()


def is_digit(string: str):
    if string.isdigit():
        return True, int(string)
    no_punctuation = string.replace(" ", "").replace(".", "").replace(",", "")
    if no_punctuation.isdigit():
        return True, int(no_punctuation)
    return False, no_punctuation
