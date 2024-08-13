import os
import re

def create_directories(language):
    """
    Create necessary directories for storing intermediate files and results.

    Parameters:
    language (str): The language for which directories are being created.

    Returns:
    str: The base path where directories are created.
    """
    base_path = os.path.join(language)
    os.makedirs(os.path.join(base_path, "bpe_operations"), exist_ok=True)
    os.makedirs(os.path.join(base_path, "correct_segmentations"), exist_ok=True)
    os.makedirs(os.path.join(base_path, "segmented_corpus"), exist_ok=True)
    return base_path

def words_from_file(filename, corpus_path):
    """
    Extract words from the given file and write them to a corpus file.

    Parameters:
    filename (str): The input filename to read words from.
    corpus_path (str): The output path to write the corpus file.

    Returns:
    list: A list of words extracted from the file.
    """
    words = []
    with open(filename, "r", encoding="UTF-8") as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            phrase = lines[i].strip().replace('-', '').split()
            words.extend(phrase)
    with open(corpus_path, "w", encoding="UTF-8") as output_file:
        for word in words:
            output_file.write(word + "\n")
    return words

def words_from_file_regex(filename, segmented_path):
    """
    Extract words using regex from the given file and write them to a segmented file.

    Parameters:
    filename (str): The input filename to read words from.
    segmented_path (str): The output path to write the segmented words.

    Returns:
    str: The path to the segmented file.
    """
    with open(filename, "r", encoding="UTF-8") as file:
        lines = file.readlines()
        with open(segmented_path, "w", encoding="UTF-8") as output_file:
            for i in range(0, len(lines), 3):
                phrase = lines[i].strip()
                for word in re.findall(r"\S+", phrase):
                    word_without_hyphen = word.replace("-", " ")
                    output_file.write(f"{word_without_hyphen}\n")
    return segmented_path  # Ensure the path to the output file is returned

def calculate_frequencies(tokenized_file):
    """
    Calculate the frequency of words in a tokenized file.

    Parameters:
    tokenized_file (str): The path to the tokenized file.

    Returns:
    Counter: A Counter object with word frequencies.
    """
    from collections import Counter

    with open(tokenized_file, "r", encoding="UTF-8") as file:
        words = file.read().split()
    return Counter(words)

def calculate_initial_vocab_size(filename):
    words = []
    with open(filename, "r", encoding="UTF-8") as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            phrase = lines[i].strip().replace('-', '').split()
            words.extend(phrase)
    return len(set(words))
