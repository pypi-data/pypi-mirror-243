import bz2
import csv
import io
import json
import pathlib
import urllib.request

# TODO: check for hash update

# Published market type ids
url = "https://www.fuzzwork.co.uk/dump/latest/invTypes.csv.bz2"
response = urllib.request.urlopen(url)
content = response.read()
decompressed = bz2.decompress(content)
file = io.StringIO(decompressed.decode())
reader = csv.reader(file)

type_ids = set()
header = next(reader)
for row in reader:
    type_id, _, _, _, _, _, _, _, _, _, published, market_group_id, _, _, _ = row
    if published == "1" and market_group_id != "None":
        type_ids.add(int(type_id))
file.close()

# Casefolded meta groups and type names with type ids
url = "https://www.fuzzwork.co.uk/dump/latest/trnTranslations.csv.bz2"
response = urllib.request.urlopen(url)
content = response.read()
decompressed = bz2.decompress(content)
file = io.StringIO(decompressed.decode())
reader = csv.reader(file)

meta_groups = set()
type_name_and_id = set()
header = next(reader)
for row in reader:
    tcID, keyID, _, text = row
    if tcID == "8" and int(keyID) in type_ids:
        type_name_and_id.add((text.casefold(), keyID))
    elif tcID == "34":
        meta_groups.add(text.casefold())
file.close()

TYPE_NAMES_PATH = pathlib.Path(__file__).resolve().parent / "type_names.json"
META_GROUPS_PATH = pathlib.Path(__file__).resolve().parent / "meta_groups.json"

with META_GROUPS_PATH.open("w") as file:
    json.dump(list(meta_groups), file)

with TYPE_NAMES_PATH.open("w") as file:
    json.dump(dict(type_name_and_id), file)

# TODO: write new hash
