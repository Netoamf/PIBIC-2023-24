import re
import collections

def initialize_vocabulary(word_freq):
    """
    Initializes the vocabulary with word frequencies.

    Args:
        word_freq (dict): Dictionary of words and their frequencies.

    Returns:
        dict: Initialized vocabulary.
    """
    vocab = {' '.join(word): freq for word, freq in word_freq.items()}
    return vocab

def get_stats(vocab):
    """
    Computes pair statistics for the given vocabulary.

    Args:
        vocab (dict): Vocabulary with word frequencies.

    Returns:
        dict: Dictionary of symbol pairs and their frequencies.
    """
    pairs = collections.defaultdict(int)
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            pairs[(symbols[i], symbols[i + 1])] += freq
    return pairs

def merge_vocab(pair, vocab):
    """
    Merges the most frequent pair in the vocabulary.

    Args:
        pair (tuple): The pair to merge.
        vocab (dict): The current vocabulary.

    Returns:
        dict: Updated vocabulary with the pair merged.
    """
    new_vocab = {}
    bigram = ' '.join(pair)
    replacement = ''.join(pair)
    for word in vocab:
        new_word = re.sub(bigram, replacement, word)
        new_vocab[new_word] = vocab[word]
    return new_vocab

def learn_bpe(word_freq, num_merges):
    """
    Learns Byte Pair Encoding (BPE) for the given word frequencies.

    Args:
        word_freq (dict): Dictionary of word frequencies.
        num_merges (int): Number of merge operations.

    Returns:
        list: List of BPE merge operations.
        dict: Final vocabulary after merges.
    """
    vocab = initialize_vocabulary(word_freq)
    bpe_codes = []
    for i in range(num_merges):
        pairs = get_stats(vocab)
        if not pairs:
            break
        best_pair = max(pairs, key=pairs.get)
        vocab = merge_vocab(best_pair, vocab)
        bpe_codes.append(best_pair)
    return bpe_codes, vocab

def apply_bpe(word, bpe_codes):
    """
    Applies Byte Pair Encoding (BPE) to a given word.

    Args:
        word (str): The word to apply BPE to.
        bpe_codes (list): List of BPE merge operations.

    Returns:
        list: List of BPE tokens.
    """
    word = ' '.join(word)
    for pair in bpe_codes:
        bigram = ' '.join(pair)
        replacement = ''.join(pair)
        word = re.sub(bigram, replacement, word)
    return word.split()

def tokenize_corpus(text, bpe_codes):
    """
    Tokenizes a text corpus using BPE.

    Args:
        text (str): The text corpus to tokenize.
        bpe_codes (list): List of BPE merge operations.

    Returns:
        set: Set of BPE tokens.
    """
    words = text.split()
    tokens = set()
    for word in words:
        tokens.update(apply_bpe(word, bpe_codes))
    return tokens
