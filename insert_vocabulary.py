import json


def get_user_input():
    # get chapter and next id from user
    with open("dictionary.json") as f:
        dict = json.load(f)
        max_chapter = int(
            max(dict["vocabulary"], key=lambda a: int(a["chapter"]))["chapter"]
        )
        max_id = int(max(dict["vocabulary"], key=lambda a: int(a["id"]))["id"])
    chapter = input(f"chapter ({max_chapter + 1}): ")
    next_id = input(f"next id ({max_id + 1}): ")

    # verify chapter and next_id
    if not chapter:
        chapter = max_chapter + 1
    if not next_id:
        next_id = max_id + 1
    chapter = int(chapter)
    next_id = int(next_id)
    print()

    return {"chapter": chapter, "next_id": next_id}


def parse_vocab(vocab, id, chapter):
    # verify the passed vocab
    parsed_vocab = vocab.split(";")
    if len(parsed_vocab) != 2:
        return False

    # vocab is correct, add to the dictionary
    with open("dictionary.json") as f:
        dict = json.load(f)
    obj = {
        "id": str(id),
        "chapter": str(chapter),
        "romaji": parsed_vocab[0].strip(),
        "dutch": parsed_vocab[1].strip(),
    }
    dict["vocabulary"].append(obj)
    with open("dictionary.json", "w") as f:
        json.dump(dict, f, indent=2)

    return True


def main():
    user_input = get_user_input()
    chapter = user_input["chapter"]
    next_id = user_input["next_id"]
    with open("dictionary.json") as f:
        dict = json.load(f)
    chapter_text = list(
        filter(lambda a: a["id"] == str(chapter), dict["chapters"])
    )
    chapter_text = chapter_text[0]["name"] if len(chapter_text) else ""
    print(f"next chapter: {chapter} ({chapter_text})")
    print(f"next id: {next_id}")
    print()
    print("add words by entering 'romaji;dutch' on every new line:")

    next_vocab = input(f"next id = {next_id}: ")
    while next_vocab:
        if parse_vocab(next_vocab, next_id, chapter):
            next_id += 1
        else:
            print("invalid input, retry...")
        next_vocab = input(f"next id = {next_id}: ")


if __name__ == "__main__":
    main()