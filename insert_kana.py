import json


def get_user_input(kana):
    # get next id from user
    with open("dictionary.json") as f:
        _dict = json.load(f)
        max_id = 0
        for obj in _dict["vocabulary"]:
            max_id = obj["id"] if kana in obj else max_id
        max_id = int(max_id["id"] if type(max_id) == dict else max_id)
    next_id = input(f"next id ({max_id + 1}): ")

    # verify next_id
    if not next_id:
        next_id = max_id + 1
    next_id = int(next_id)
    print()

    return {"next_id": next_id}


def parse_vocab(vocab, id, kana):
    with open("dictionary.json") as f:
        _dict = json.load(f)
    for obj in _dict["vocabulary"]:
        if str(id) == obj["id"]:
            obj[kana] = vocab
    with open("dictionary.json", "w") as f:
        json.dump(_dict, f, indent=2)

    return True


def get_next_id(next_id):
    with open("dictionary.json") as f:
        _dict = json.load(f)
        res = list(
            filter(lambda a: a["id"] == str(next_id), _dict["vocabulary"])
        )
        romaji = res[0]["romaji"] if res else ""
    return f"next id = {next_id} ({romaji}): "


def main():
    kana = input("which kana? [hiragana/kanji]: ")
    user_input = get_user_input(kana)
    next_id = user_input["next_id"]
    print(f"next id: {next_id}")
    print()
    print(f"add words by entering '{kana}' on every new line:")

    next_vocab = input(get_next_id(next_id))
    while next_vocab:
        if parse_vocab(next_vocab, next_id, kana):
            next_id += 1
        else:
            print("invalid input, retry...")
        next_vocab = input(get_next_id(next_id))


if __name__ == "__main__":
    main()
