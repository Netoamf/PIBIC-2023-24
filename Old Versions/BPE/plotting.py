import matplotlib.pyplot as plt
import seaborn as sns

def plot_coverage_and_compression(coverage_results, accuracy_results):
    """
    Plots coverage, compression, and accuracy results.

    Args:
        coverage_results (list): Coverage results.
        accuracy_results (list): Accuracy results.

    Returns:
        None
    """
    merges, coverage, compression = zip(*coverage_results)
    _, accuracy = zip(*accuracy_results)
    
    fig, ax1 = plt.subplots(figsize=(12, 8))

    ax1.set_xscale('log', base=2)
    ax1.set_xlabel('Number of Merges (log scale)')
    
    ax1.set_ylabel('Vocabulary Coverage', color='tab:blue')
    ax1.plot(merges, coverage, marker='o', color='tab:blue', label='Coverage')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Compression Ratio', color='tab:red')
    ax2.plot(merges, compression, marker='o', color='tab:red', label='Compression')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    ax3 = ax1.twinx()
    ax3.set_ylabel('Segmentation Accuracy', color='tab:green')
    ax3.plot(merges, accuracy, marker='o', color='tab:green', label='Accuracy')
    ax3.tick_params(axis='y', labelcolor='tab:green')

    fig.tight_layout()
    plt.title('Vocabulary Coverage, Compression Ratio, and Segmentation Accuracy vs. Number of Merges')
    plt.show()

def plot_token_length_distribution(token_lengths):
    """
    Plots the distribution of token lengths.

    Args:
        token_lengths (list): List of token lengths.

    Returns:
        None
    """
    plt.figure(figsize=(14, 7))
    sns.histplot(token_lengths, bins=20, kde=True)
    plt.title('Token Length Distribution')
    plt.xlabel('Token Length')
    plt.ylabel('Frequency')
    plt.show()
