import json
import logging
import os
from corpus_creation import words_from_file, extract_morphemes_from_file
from corpus import read_corpus, normalize_text, count_word_frequencies
from bpe import learn_bpe, tokenize_corpus, apply_bpe, initialize_vocabulary
from analysis import (
    save_tokens_with_words, save_matched_segmented_words, calculate_compression_ratio,
    vocabulary_coverage, analyze_coverage_log, analyze_accuracy_log, save_results_to_csv,
    token_frequency_distribution, token_length_distribution, calculate_entropy,
    segment_sentence, compare_tokens_with_segmented_words, save_correct_segmentations
)
from plotting import plot_coverage_and_compression, plot_token_length_distribution

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_path):
    """
    Loads the configuration from a JSON file.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        dict: Configuration dictionary, or None if an error occurs.
    """
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        logging.error(f"Error loading config file: {e}")
        return None

def main():
    """
    Executes the BPE pipeline.

    Returns:
        None
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config.json')
    logging.info(f"Current directory: {os.getcwd()}")
    logging.info(f"Looking for config file at: {config_path}")

    config = load_config(config_path)
    if not config:
        return

    corpus_file = config['corpus_file']
    morphemes_file = config['morphemes_file']
    segmented_words_file = config['segmented_words_file']
    output_results_file = config['output_results_file']
    output_tokens_file = config['output_tokens_file']
    output_matches_file = config['output_matches_file']
    output_correct_segmentations_file = config['output_correct_segmentations_file']
    max_merges = config['max_merges']

    logging.info("Reading and normalizing corpus")
    corpus_text = read_corpus(corpus_file)
    if corpus_text is None:
        logging.error("Failed to read corpus file")
        return
    normalized_text = normalize_text(corpus_text)
    
    logging.info("Counting word frequencies")
    word_freq = count_word_frequencies(normalized_text)
    
    logging.info("Reading morphemes and segmented words")
    morphemes_text = read_corpus(morphemes_file)
    morphemes_from_text = morphemes_text.split()

    segmented_words_text = read_corpus(segmented_words_file)
    segmented_words = segmented_words_text.splitlines()
    
    logging.info("Analyzing coverage and accuracy")
    coverage_results = analyze_coverage_log(word_freq, morphemes_from_text, max_merges)
    accuracy_results = analyze_accuracy_log(word_freq, segmented_words, max_merges)
    
    logging.info("Saving results to CSV")
    save_results_to_csv(coverage_results, accuracy_results, output_results_file)
    
    logging.info("Plotting coverage and compression")
    plot_coverage_and_compression(coverage_results, accuracy_results)
    
    num_merges = 1024
    bpe_codes, final_vocab = learn_bpe(word_freq, num_merges)
    
    logging.info("Tokenizing corpus")
    tokens = tokenize_corpus(normalized_text, bpe_codes)
    
    logging.info("Saving tokens with words")
    save_tokens_with_words(tokens, word_freq.keys(), output_tokens_file)
    
    original_vocab = initialize_vocabulary(word_freq)
    compression_ratio = calculate_compression_ratio(original_vocab, final_vocab)
    logging.info(f"Compression Ratio: {compression_ratio:.2f}")
    
    coverage = vocabulary_coverage(tokens, morphemes_from_text)
    logging.info(f"Vocabulary Coverage: {coverage:.2%}")
    
    logging.info("Saving matched segmented words")
    save_matched_segmented_words(morphemes_from_text, tokens, output_matches_file)

    token_freq = token_frequency_distribution(tokens)
    token_lengths = token_length_distribution(tokens)
    entropy = calculate_entropy(token_freq)
    
    logging.info(f"Entropy: {entropy:.2f}")

    logging.info("Plotting token length distribution")
    plot_token_length_distribution(token_lengths)
    
    correct_segmentations, accuracy = compare_tokens_with_segmented_words(bpe_codes, segmented_words)
    save_correct_segmentations(correct_segmentations, output_correct_segmentations_file)
    
    logging.info(f"Segmentation Accuracy: {accuracy:.2%}")
    
    while True:
        user_sentence = input("Digite uma frase para segmentação morfológica (ou 'sair' para encerrar): ")
        if user_sentence.lower() == 'sair':
            break
        
        segmented_sentence = segment_sentence(user_sentence, bpe_codes)
        
        print("Frase segmentada morfologicamente:", segmented_sentence)

if __name__ == "__main__":
    main()
