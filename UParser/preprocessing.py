# preprocessing.py
import re

def preprocess_corpus(corpus_path):
    """
    Preprocess the corpus by removing punctuation and converting to lowercase.

    Parameters:
    corpus_path (str): The path to the corpus file to preprocess.
    """
    with open(corpus_path, 'r', encoding='UTF-8') as file:
        content = file.read()

    # Remove general punctuation marks and convert to lowercase
    content = re.sub(r'[.,"()?¿?¡!»«“”،/\\]', '', content).lower()

    with open(corpus_path, 'w', encoding='UTF-8') as file:
        file.write(content)
