import json


def get_user_input(course):
    # get chapter and next id from user
    with open("dictionary.json") as f:
        dict = json.load(f)
        max_chapter = 0
        max_id = 0
        # ugly last chapter/id fetching
        last_item = dict["vocabulary"][-1]
        if last_item["course"] == f"{course}":
            max_chapter = int(last_item["chapter"][5:])
            max_id = int(last_item["id"][5:])
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


def parse_vocab(vocab, id, chapter, course, fields_to_enter):
    # verify the passed vocab
    parsed_vocab = vocab.split(";")
    fields_to_enter = fields_to_enter.split(";")
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
    course = "jem2"
    override_course = input(f"course ({course}): ")
    if override_course:
        course = override_course
    user_input = get_user_input(course)
    chapter = user_input["chapter"]
    next_id = user_input["next_id"]
    fields_to_enter = input(
        "enter fields to be entered separated by ';' "
        "(e.g. romaji;dutch;hiragana): "
    )
    with open("dictionary.json") as f:
        dict = json.load(f)
    chapter_text = list(
        filter(lambda a: a["id"] == f"{course}-{chapter}", dict["chapters"])
    )
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
