import matplotlib.pyplot as plt
import os
def plot_coverage_vs_merges(coverage_data, language):
    """
    Plot coverage vs. number of BPE merges.

    Parameters:
    coverage_data (list): List of tuples with (number of merges, coverage).
    language (str): The language being analyzed.
    """
    merges, coverages = zip(*coverage_data)
    plt.figure()
    plt.plot(merges, coverages, marker='o')
    plt.xlabel('Number of BPE Merges')
    plt.ylabel('Coverage (%)')
    plt.title(f'Coverage vs. Number of BPE Merges for {language}')
    plt.grid(True)
    plt.savefig(os.path.join(language, 'coverage_vs_merges.png'))
    plt.show()

def plot_compression_vs_coverage(compression_data, language):
    """
    Plot vocabulary compression vs. coverage.

    Parameters:
    compression_data (list): List of tuples with (compression, coverage).
    language (str): The language being analyzed.
    """
    compressions, coverages = zip(*compression_data)
    plt.figure()
    plt.plot(compressions, coverages, marker='o')
    plt.xlabel('Vocabulary Compression (%)')
    plt.ylabel('Coverage (%)')
    plt.title(f'Vocabulary Compression vs. Coverage for {language}')
    plt.grid(True)
    plt.savefig(os.path.join(language, 'compression_vs_coverage.png'))
    plt.show()

def plot_frequent_segments_vs_merges(segment_data, language):
    """
    Plot most frequent segments vs. number of merges.

    Parameters:
    segment_data (list): List of tuples with (segment, number of merges).
    language (str): The language being analyzed.
    """
    segments, merges = zip(*segment_data)
    unique_segments = list(set(segments))
    plt.figure()
    for segment in unique_segments:
        merge_points = [m for s, m in segment_data if s == segment]
        plt.plot(merge_points, [segment] * len(merge_points), 'o', label=segment)
    plt.xlabel('Merge Round')
    plt.ylabel('Segment')
    plt.title(f'Most Frequent Segments vs. Merges for {language}')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(language, 'frequent_segments_vs_merges.png'))
    plt.show()

