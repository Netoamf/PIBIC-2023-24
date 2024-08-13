# segmentation.py
import subprocess

def train_bpe(corpus_path, bpe_operations_path, num_merges):
    """
    Train Byte Pair Encoding (BPE) on the given corpus.

    Parameters:
    corpus_path (str): The path to the corpus file.
    bpe_operations_path (str): The path to save BPE operations.
    num_merges (int): The number of BPE merge operations.

    Returns:
    bool: True if training is successful, False otherwise.
    """
    try:
        subprocess.run([
            'subword-nmt', 'learn-bpe', '-s', str(num_merges), '--input', corpus_path, '--output', bpe_operations_path
        ], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during BPE learning with {num_merges} merges: {e}")
        return False

def apply_bpe(corpus_path, bpe_operations_path, output_segmented_corpus_path, num_merges):
    """
    Apply Byte Pair Encoding (BPE) to the corpus using the specified number of merges.

    Parameters:
    corpus_path (str): The path to the corpus file.
    bpe_operations_path (str): The path to the BPE operations file.
    output_segmented_corpus_path (str): The path to save the segmented corpus.
    num_merges (int): The number of BPE merge operations.

    Returns:
    bool: True if application is successful, False otherwise.
    """
    if num_merges == 0:
        with open(corpus_path, 'r', encoding='UTF-8') as infile, open(output_segmented_corpus_path, 'w', encoding='UTF-8') as outfile:
            outfile.write(infile.read())
        return True
    else:
        try:
            subprocess.run([
                'subword-nmt', 'apply-bpe', '-c', bpe_operations_path, '--input', corpus_path, '--output', output_segmented_corpus_path
            ], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error during BPE application with {num_merges} merges: {e}")
            return False

def compare_segments(bpe_segments, segmented_words):
    """
    Compare BPE segments with linguist's segments and identify correct segmentations.

    Parameters:
    bpe_segments (list): List of BPE segmented words.
    segmented_words (list): List of linguist's segmented words.

    Returns:
    list: A list of tuples with correctly segmented words.
    """
    correct_segmentations = []
    for bpe_seg, ling_seg in zip(bpe_segments, segmented_words):
        bpe_seg_cleaned = bpe_seg.strip().replace('@@ ', '').replace(' ', '')
        ling_seg_cleaned = ling_seg.strip().replace(' ', '')
        if bpe_seg_cleaned == ling_seg_cleaned and bpe_seg.strip().replace('@@', ' ') == ling_seg.strip():
            correct_segmentations.append((bpe_seg.strip(), ling_seg.strip()))
    return correct_segmentations

def save_correct_segmentations(correct_segmentations, file_path):
    """
    Save correct segmentations to a file.

    Parameters:
    correct_segmentations (list): List of correctly segmented words.
    file_path (str): Path to save the correct segmentations.
    """
    with open(file_path, "w", encoding="UTF-8") as file:
        for bpe_seg, ling_seg in correct_segmentations:
            file.write(f"BPE: {bpe_seg} | Linguist: {ling_seg}\n")
