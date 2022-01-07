import json


def get_user_input(course, kana):
    # get next id from user
    with open("dictionary.json") as f:
        _dict = json.load(f)
        max_id = -1
        for obj in _dict["vocabulary"]:
            if kana in obj and f"{course}-" in obj["id"]:
                try:
                    max_id = max(int(obj["id"][5:]), max_id)
                except:
                    pass
    next_id = input(f"next id ({max_id + 1}): ")

    # verify next_id
    if not next_id:
        next_id = max_id + 1
    next_id = int(next_id)
    print()

    return {"next_id": next_id}


def parse_vocab(course, vocab, id, kana):
    with open("dictionary.json") as f:
        _dict = json.load(f)
    for obj in _dict["vocabulary"]:
        if f"{course}-{id}" == obj["id"]:
            obj[kana] = vocab
    with open("dictionary.json", "w") as f:
        json.dump(_dict, f, indent=2)

    return True


def get_next_id(course, next_id):
    with open("dictionary.json") as f:
        _dict = json.load(f)
        res = list(
            filter(lambda a: a["id"] == f"{course}-{next_id}", _dict["vocabulary"])
        )
        hiragana = res[0]["hiragana"] if res else ""
        romaji = res[0]["romaji"] if res else ""
        info = "/".join([hiragana, romaji])
    return f"next id = {next_id} ({info}): "


def main():
    course = "jem1"
    override_course = input(f"course ({course}): ")
    if override_course:
        course = override_course
    kana = input("which kana? [hiragana/kanji]: ")
    user_input = get_user_input(course, kana)
    next_id = user_input["next_id"]
    print(f"next id: {next_id}")
    print()
    print(f"add words by entering '{kana}' on every new line:")

    next_vocab = input(get_next_id(course, next_id))
    while next_vocab:
        if parse_vocab(course, next_vocab, next_id, kana):
            next_id += 1
        else:
            print("invalid input, retry...")
        next_vocab = input(get_next_id(course, next_id))


if __name__ == "__main__":
    main()
