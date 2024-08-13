import re
import collections

def read_corpus(file_path):
    """
    Reads the text content from a file.

    Args:
        file_path (str): The path to the file containing the corpus.

    Returns:
        str: The text content of the file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def normalize_text(text):
    """
    Normalizes the text by converting it to lowercase and removing non-alphanumeric characters.

    Args:
        text (str): The text to normalize.

    Returns:
        str: The normalized text.
    """
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def count_word_frequencies(text):
    """
    Counts the frequency of each word in the text.

    Args:
        text (str): The text to analyze.

    Returns:
        collections.Counter: A Counter object with word frequencies.
    """
    words = text.split()
    word_freq = collections.Counter(words)
    return word_freq
