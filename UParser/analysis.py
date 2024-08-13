from segmentation import compare_segments

def calculate_coverage(bpe_segments, segmented_words):
    """
    Calculate the coverage of BPE segments against linguist's segments.

    Parameters:
    bpe_segments (list): List of BPE segmented words.
    segmented_words (list): List of linguist's segmented words.

    Returns:
    float: The coverage percentage.
    """
    correct_segmentations = compare_segments(bpe_segments, segmented_words)
    return len(correct_segmentations) / len(bpe_segments) * 100



def calculate_compression_ratio(initial_vocab_size, final_vocab_size):
    """
    Calculates the compression ratio of the vocabulary.

    Args:
        initial_vocab_size (int): Initial size of the vocabulary.
        final_vocab_size (int): Final size of the vocabulary after BPE merges.

    Returns:
        float: Compression ratio.
    """
    return (1 - (final_vocab_size / initial_vocab_size)) * 100


