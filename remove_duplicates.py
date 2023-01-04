import json


def word_equal(word1: "dict[str, str]", word2: "dict[str, str]"):
    equal_keys: list[str] = ["dutch", "hiragana", "romaji", "nihongo"]
    words_are_equal = all(word1[key] == word2[key] for key in equal_keys)
    return words_are_equal


def word_japanese_equal(word1: "dict[str, str]", word2: "dict[str, str]"):
    equal_keys: list[str] = ["hiragana", "romaji", "nihongo"]
    words_are_equal = all(word1[key] == word2[key] for key in equal_keys)
    if words_are_equal:
        print(word1, word2, sep="\n")
    return words_are_equal


def word_equal_in(word1: "dict[str, str]", word2: "dict[str, str]", key):
    words_are_equal = word1[key] == word2[key]
    if words_are_equal:
        print(word1, word2, sep="\n")
    return words_are_equal


def check_remove(vocabulary: "list[dict[str, str]]", word: "dict[str, str]"):
    while response := input("remove word? [y/N] "):
        if response.lower() == "y":
            vocabulary.remove(word)
            write_dictionary(vocabulary)
            break
        elif response.lower() == "n":
            break


def main():
    from_course = "jem-old-1"

    with open("dictionary.json") as f:
        vocabulary: list[dict[str, str]] = json.load(f)["vocabulary"]
    from_words: list[dict[str, str]] = [entry for entry in vocabulary if entry["course"] == from_course]
    rest_words: list[dict[str, str]] = [entry for entry in vocabulary if entry["course"] != from_course]
    assert len(from_words) + len(rest_words) == len(vocabulary)

    len_before_pruning = len(from_words)
    for word in from_words:
        if any(word_equal(word, rest_word) for rest_word in rest_words):
            print(f"removing duplicate word: {word['id']}")
            vocabulary.remove(word)
            write_dictionary(vocabulary)
    from_words: list[dict[str, str]] = [entry for entry in vocabulary if entry["course"] == from_course]
    print(f"pruned {len_before_pruning-len(from_words)} words")

    japanese_equal_words = 0
    for word in from_words:
        if any(word_japanese_equal(word, rest_word) for rest_word in rest_words):
            print(f"found equal in japanese word: {word['id']}")
            check_remove(vocabulary, word)
            japanese_equal_words += 1
    from_words: list[dict[str, str]] = [entry for entry in vocabulary if entry["course"] == from_course]
    print(f"words equal in japanese: {japanese_equal_words}")

    for key in ["hiragana", "romaji", "nihongo"]:
        equal_words = 0
        for word in from_words:
            if any(word_japanese_equal(word, rest_word) for rest_word in rest_words):
                print(f"found equal in {key} word: {word['id']}")
                check_remove(vocabulary, word)
                equal_words += 1
        from_words: list[dict[str, str]] = [entry for entry in vocabulary if entry["course"] == from_course]
        print(f"words equal in {key}: {equal_words}")

    print(f"words left: {len(from_words)}")

    write_dictionary(vocabulary)


def write_dictionary(vocabulary: "list[dict[str, str]]"):
    with open("dictionary.json") as f:
        dictionary = json.load(f)
    dictionary["vocabulary"] = vocabulary
    with open("dictionary.json", "w") as f:
        json.dump(dictionary, f, indent=2)


if __name__ == "__main__":
    main()
