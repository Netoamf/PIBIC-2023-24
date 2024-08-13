import csv
import collections
import math
from bpe import apply_bpe, learn_bpe, tokenize_corpus, initialize_vocabulary
from corpus import normalize_text, read_corpus

def save_tokens_with_words(tokens, original_words, file_path):
    """
    Saves tokens with their corresponding original words to a file.

    Args:
        tokens (set): Set of tokens.
        original_words (iterable): Original words.
        file_path (str): Path to the output file.

    Returns:
        None
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        for word in original_words:
            tokenized_word = ' '.join(apply_bpe(word, tokens))
            f.write(f"{word}: {tokenized_word}\n")

def save_matched_segmented_words(segmented_words, tokens, file_path):
    """
    Saves matched segmented words to a file.

    Args:
        segmented_words (iterable): Segmented words.
        tokens (set): Set of tokens.
        file_path (str): Path to the output file.

    Returns:
        None
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        for word in segmented_words:
            if all(token in tokens for token in word.split()):
                f.write(word + '\n')

def calculate_compression_ratio(original_vocab, final_vocab):
    """
    Calculates the compression ratio of the vocabulary.

    Args:
        original_vocab (dict): Original vocabulary.
        final_vocab (dict): Final vocabulary after BPE merges.

    Returns:
        float: Compression ratio.
    """
    original_size = sum(len(word) for word in original_vocab.keys())
    final_size = sum(len(word) for word in final_vocab.keys())
    return original_size / final_size

def vocabulary_coverage(tokens, segmented_words):
    """
    Calculates the vocabulary coverage.

    Args:
        tokens (set): Set of tokens.
        segmented_words (iterable): Segmented words.

    Returns:
        float: Vocabulary coverage.
    """
    covered_words = [word for word in segmented_words if all(token in tokens for token in word.split())]
    return len(covered_words) / len(segmented_words)

def analyze_coverage_log(word_freq, segmented_words, max_merges):
    """
    Analyzes coverage and compression over multiple merge steps.

    Args:
        word_freq (dict): Dictionary of word frequencies.
        segmented_words (iterable): Segmented words.
        max_merges (int): Maximum number of merges.

    Returns:
        list: Coverage results.
    """
    coverage_results = []
    num_merges = 1
    while num_merges <= max_merges:
        bpe_codes, final_vocab = learn_bpe(word_freq, num_merges)
        tokens = tokenize_corpus(normalize_text(read_corpus('corpus.txt')), bpe_codes)
        coverage = vocabulary_coverage(tokens, segmented_words)
        compression_ratio = calculate_compression_ratio(initialize_vocabulary(word_freq), final_vocab)
        coverage_results.append((num_merges, coverage, compression_ratio))
        print(f"Merges: {num_merges}, Coverage: {coverage:.2%}, Compression: {compression_ratio:.2f}")
        num_merges *= 2
    return coverage_results

def analyze_accuracy_log(word_freq, segmented_words, max_merges):
    """
    Analyzes accuracy over multiple merge steps.

    Args:
        word_freq (dict): Dictionary of word frequencies.
        segmented_words (iterable): Segmented words.
        max_merges (int): Maximum number of merges.

    Returns:
        list: Accuracy results.
    """
    accuracy_results = []
    num_merges = 1
    while num_merges <= max_merges:
        bpe_codes, _ = learn_bpe(word_freq, num_merges)
        accuracy = compare_tokens_with_segmented_words(bpe_codes, segmented_words)[1]
        accuracy_results.append((num_merges, accuracy))
        print(f"Merges: {num_merges}, Accuracy: {accuracy:.2%}")
        num_merges *= 2
    return accuracy_results

def save_results_to_csv(coverage_results, accuracy_results, file_path):
    """
    Saves coverage and accuracy results to a CSV file.

    Args:
        coverage_results (list): Coverage results.
        accuracy_results (list): Accuracy results.
        file_path (str): Path to the output CSV file.

    Returns:
        None
    """
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['num_merges', 'coverage', 'compression_ratio', 'accuracy']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for (num_merges, coverage, compression_ratio), (_, accuracy) in zip(coverage_results, accuracy_results):
            writer.writerow({'num_merges': num_merges, 'coverage': coverage, 'compression_ratio': compression_ratio, 'accuracy': accuracy})

def token_frequency_distribution(tokens):
    """
    Computes the frequency distribution of tokens.

    Args:
        tokens (set): Set of tokens.

    Returns:
        collections.Counter: Token frequency distribution.
    """
    token_freq = collections.Counter(tokens)
    return token_freq

def token_length_distribution(tokens):
    """
    Computes the length distribution of tokens.

    Args:
        tokens (set): Set of tokens.

    Returns:
        list: Token lengths.
    """
    token_lengths = [len(token) for token in tokens]
    return token_lengths

def calculate_entropy(token_freq):
    """
    Calculates the entropy of the token frequency distribution.

    Args:
        token_freq (collections.Counter): Token frequency distribution.

    Returns:
        float: Entropy.
    """
    total_tokens = sum(token_freq.values())
    entropy = -sum((count / total_tokens) * math.log(count / total_tokens, 2) for count in token_freq.values())
    return entropy

def segment_sentence(sentence, bpe_codes):
    """
    Segments a sentence using BPE codes.

    Args:
        sentence (str): The sentence to segment.
        bpe_codes (list): List of BPE merge operations.

    Returns:
        list: List of segmented words.
    """
    normalized_sentence = normalize_text(sentence)
    words = normalized_sentence.split()
    segmented_sentence = [apply_bpe(word, bpe_codes) for word in words]
    return segmented_sentence

def compare_tokens_with_segmented_words(bpe_codes, segmented_words):
    """
    Compares tokens with segmented words to evaluate accuracy.

    Args:
        bpe_codes (list): List of BPE merge operations.
        segmented_words (iterable): Segmented words.

    Returns:
        list: Correct segmentations.
        float: Accuracy.
    """
    correct_segmentations = []
    total_words = len(segmented_words)
    
    for word in segmented_words:
        original_word = word.replace(' ', '')
        tokenized_word = ' '.join(apply_bpe(original_word, bpe_codes))
        if tokenized_word == word:
            correct_segmentations.append(f"{original_word}: {tokenized_word}")
    
    accuracy = len(correct_segmentations) / total_words
    return correct_segmentations, accuracy

def save_correct_segmentations(correct_segmentations, file_path):
    """
    Saves correct segmentations to a file.

    Args:
        correct_segmentations (list): List of correct segmentations.
        file_path (str): Path to the output file.

    Returns:
        None
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in correct_segmentations:
            f.write(item + '\n')
