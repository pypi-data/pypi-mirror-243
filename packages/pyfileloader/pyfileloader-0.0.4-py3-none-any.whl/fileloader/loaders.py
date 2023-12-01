import csv
import json
import sys
import gzip


def load_json(file: str):
    openfn = open
    needs_decode = False
    if file.endswith("gz"):
        openfn = gzip.open
        needs_decode = True

    with openfn(file, "r") as f:
        data = f.read()
    if needs_decode:
        data = data.decode("UTF-8")

    item = json.load(data)
    return item


def load_jsonl(file: str):
    lines = load_text(file)
    items = []
    for line in lines:
        items.append(json.loads(line))

    return items


def load_text(file: str):
    openfn = open
    needs_decode = False
    if file.endswith("gz"):
        openfn = gzip.open
        needs_decode = True

    items = []
    with openfn(file, "r") as f:
        for line in f:
            if needs_decode:
                line = line.decode("UTF-8")

            items.append(line.strip())

    return items


def load_csv(file: str):
    openfn = open

    # the resulting binary stream when opening with gzip.open needs to be handled
    # in a different manner than the other functions

    if file.endswith("gz"):
        print("Unsupported .gz extension. Manually gunzip first")
        sys.exit(1)

    items = []
    file_csv = csv.DictReader(openfn(file, "r"))
    for row in file_csv:
        items.append(row.decode("UTF-8"))

    return items


if __name__ == "__main__":

    # lines = load_text(sys.argv[1])
    lines = load_csv(sys.argv[1])

    print(lines)
