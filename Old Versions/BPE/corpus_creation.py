import re

def words_from_file(filename):
    """
    Extracts words from an input file and writes them to a corpus file.

    Args:
        filename (str): grammar file
    Returns:
        None
    """
    words = []
    with open(filename, "r", encoding="UTF-8") as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            phrase = lines[i].strip().replace('-', '').split()
            words.extend(phrase)
    with open("corpus.txt", "w", encoding="UTF-8") as output_file:
        for word in words:
            output_file.write(word + "\n")

def extract_morphemes_from_file(filename):
    """
    Extracts morphemes from an input file and writes them to a morphemes file.

    Args:
        filename (str): grammar file.
    Returns:
        None
    """
    with open(filename, "r", encoding="UTF-8") as file:
        lines = file.readlines()
        with open("words.txt", "w", encoding="UTF-8") as output_file:
            for i in range(0, len(lines), 3):
                phrase = lines[i].strip()
                words = re.sub(r"-", " ", phrase).split()
                for word in words:
                    output_file.write(f"{word}\n")

def words_from_file_regex(filename):
    """
    Extracts the segmented corpus from an input file and writes them to a segmented corpus file.

    Args:
        filename (str): grammar file.
    Returns:
        None
    """
    with open(filename, "r", encoding="UTF-8") as file:
        lines = file.readlines()
        with open("corpus_segmented.txt", "w", encoding="UTF-8") as output_file:
            for i in range(0, len(lines), 3):
                phrase = lines[i].strip()
                for word in re.findall(r"\S+", phrase):
                    word_without_hyphen = word.replace("-", " ") 
                    output_file.write(f"{word_without_hyphen}\n")
