import json


def get_user_input():
    # get course chapter and next id from user
    with open("dictionary.json") as f:
        dictionary: dict = json.load(f)

    # fetch the last course
    last_course = "course"
    if dictionary.get("vocabulary"):
        last_item = dictionary["vocabulary"][-1]
        last_course = last_item["course"]
    # confirm last course by user
    course = input(f"course ({last_course}): ")
    if not course:
        course = last_course

    # fetch the last chapter/id
    max_chapter = 0
    max_id = 0
    if dictionary.get("vocabulary"):
        for entry in reversed(dictionary["vocabulary"]):
            if entry["course"] == course:
                max_chapter = int(entry["chapter"][5:])
                max_id = int(entry["id"][5:])
                break
    # confirm last chapter/id by user
    chapter = input(f"chapter ({max_chapter + 1}): ")
    if not chapter:
        chapter = max_chapter + 1
    next_id = input(f"next id ({max_id + 1}): ")
    if not next_id:
        next_id = max_id + 1

    # convert chapter and next_id to int (should be numeric)
    chapter = int(chapter)
    next_id = int(next_id)
    print()

    return {"course": course, "chapter": chapter, "next_id": next_id}


def parse_vocab(vocab, id, chapter, course, fields_to_enter):
    # verify the passed vocab
    parsed_vocab = vocab.split("|")
    fields_to_enter = fields_to_enter.split("|")
    if len(parsed_vocab) != len(fields_to_enter):
        return False

    # vocab is correct, add to the dictionary
    with open("dictionary.json") as f:
        dict = json.load(f)
    obj = {
        "id": f"{course}-{str(id)}",
        "course": course,
        "chapter": f"{course}-{str(chapter)}",
    }
    for i in range(len(parsed_vocab)):
        obj[fields_to_enter[i]] = parsed_vocab[i].strip()
    dict["vocabulary"].append(obj)
    with open("dictionary.json", "w") as f:
        json.dump(dict, f, indent=2)

    return True


def main():
    user_input = get_user_input()
    course = user_input["course"]
    chapter = user_input["chapter"]
    next_id = user_input["next_id"]
    default_fields = "dutch|hiragana|romaji|nihongo"
    fields_to_enter = input(f"enter fields to be entered separated by '|' [{default_fields}]: ")
    if not fields_to_enter:
        fields_to_enter = default_fields
    with open("dictionary.json") as f:
        dict = json.load(f)
    chapter_text = list(filter(lambda a: a["id"] == f"{course}-{chapter}", dict["chapters"]))
    chapter_text = chapter_text[0]["name"] if len(chapter_text) else ""
    print(f"next chapter: {chapter} ({chapter_text})")
    print(f"next id: {next_id}")
    print()
    print(f"add words by entering '{fields_to_enter}' on every new line:")

    next_vocab = input(f"next id = {next_id}: ")
    while next_vocab:
        if parse_vocab(next_vocab, next_id, chapter, course, fields_to_enter):
            next_id += 1
        else:
            print("invalid input, retry...")
        next_vocab = input(f"next id = {next_id}: ")


if __name__ == "__main__":
    main()
