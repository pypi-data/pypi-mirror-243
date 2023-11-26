import bz2
import contextlib
import csv
import io
import json
import pathlib
import sys
import urllib.request

BASE_PATH = pathlib.Path(__file__).resolve().parent.parent
HASH_PATH = BASE_PATH / "hash.md5"
DATA_PATH = BASE_PATH / "eveparse" / "data"
META_PATH = DATA_PATH / "meta_groups.json"
MARKET_GROUP_PATH = DATA_PATH / "market_groups.json"
TYPE_PATH = DATA_PATH / "types.json"


def request(url: str) -> bytes:
    response = urllib.request.urlopen(url=url)
    return response.read()


# Check for hash update
content = request("https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2.md5")
latest_hash = content.decode()

with HASH_PATH.open("r") as file:
    current_hash = file.read()
    if latest_hash == current_hash:
        sys.exit(0)


@contextlib.contextmanager
def read_compressed_csv(compressed_csv: bytes) -> iter:
    decompressed_csv = bz2.decompress(data=compressed_csv)
    csv_file_buffer = io.StringIO(decompressed_csv.decode())
    try:
        yield csv.reader(csv_file_buffer)
    finally:
        csv_file_buffer.close()


# Get published market type ids
inv_types_csv = request(url="https://www.fuzzwork.co.uk/dump/latest/invTypes.csv.bz2")
with read_compressed_csv(compressed_csv=inv_types_csv) as reader:
    type_ids = set()
    header = next(reader)
    for row in reader:
        type_id = row[0]
        published = row[10]
        market_group_id = row[11]
        if published == "1" and market_group_id != "None":
            type_ids.add(int(type_id))

# Extract casefolded meta group name and type names with type ids
translations_csv = request("https://www.fuzzwork.co.uk/dump/latest/trnTranslations.csv.bz2")
with read_compressed_csv(compressed_csv=translations_csv) as reader:
    market_groups = set()
    meta_groups = set()
    type_name_and_id = set()
    header = next(reader)
    for row in reader:
        tcID, keyID, _, text = row
        if tcID == "8" and int(keyID) in type_ids:
            type_name_and_id.add((text.casefold(), int(keyID)))
        elif tcID == "7":
            market_groups.add(text.casefold())
        elif tcID == "34":
            meta_groups.add(text.casefold())


def dump_json(path: pathlib.Path, data: dict | list):
    with path.open("w") as json_file:
        json.dump(data, json_file)


dump_json(path=MARKET_GROUP_PATH, data=list(market_groups))
dump_json(path=META_PATH, data=list(meta_groups))
dump_json(path=TYPE_PATH, data=dict(type_name_and_id))

with HASH_PATH.open("w") as file:
    file.write(latest_hash)
