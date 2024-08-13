import os
import matplotlib.pyplot as plt
from math import log2
from uchunker import UChunker
from utils import words_from_file, words_from_file_regex
from comparison import compare_segmentations_to_file

class Experiments:
    """
    This class executes experiments with the UChunker algorithm using different descriptive grammars,
    iterations, and numbers of new segments. It also plots the coverage results.
    """

    def __init__(self, grammars, output_dir, max_iterations=16, max_segments=1024):
        """
        Initializes the Experiments object.

        :param grammars: A list of descriptive grammar file names.
        :param output_dir: The directory where output files will be saved.
        :param max_iterations: The maximum number of iterations (logarithmically spaced).
        :param max_segments: The maximum number of new segments (logarithmically spaced).
        """
        self.grammars = grammars
        self.output_dir = output_dir
        self.max_iterations = max_iterations
        self.max_segments = max_segments
        self.results = {}

        # Ensure the output directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def run_experiments(self):
        """
        Runs experiments for each grammar with varying iterations and new segments.
        """
        for grammar in self.grammars:
            print(f"Processing grammar: {grammar}")
            self.results[grammar] = {}

            
            output_morphemes = words_from_file(grammar, os.path.join(self.output_dir, "morphemes_output.txt"))
            output_segmentations = words_from_file_regex(grammar, os.path.join(self.output_dir, "segmentations_output.txt"))
            print(f"Morphemes file saved as: {output_morphemes}")
            print(f"Segmentations file saved as: {output_segmentations}")

            output_filename = os.path.join(self.output_dir, f"compare_segmentations_{os.path.basename(grammar)}_results.txt")
            with open(output_filename, "w", encoding="utf-8") as output_file:
                for iteration in [2**i for i in range(int(log2(self.max_iterations)) + 1)]:
                    self.results[grammar][iteration] = {}
                    for n_segments in [2**j for j in range(int(log2(self.max_segments)) + 1)]:
                        print(f"Running experiment for grammar: {grammar}, iterations: {iteration}, new segments: {n_segments}")

                        # Create a new instance of the chunker for each round of n_segments
                        chunker = UChunker(grammar)
                        chunker.start(n_segments, iteration)

                        best_matches, total_morphemes = compare_segmentations_to_file(
                            chunker.lexicon, output_segmentations, output_filename
                        )
                        coverage = (best_matches / total_morphemes) * 100
                        self.results[grammar][iteration][n_segments] = coverage
                        print(f"Coverage: {coverage:.2f}%")
                        output_file.write(f"Grammar: {grammar}, Iterations: {iteration}, New Segments: {n_segments}, Coverage: {coverage:.2f}%\n")

                        # Clear chunker memory
                        del chunker

        # Ensure the results are returned as a dictionary
        return self.results

    def plot_results(self):
        """
        Plots the coverage results for each grammar.
        """
        for grammar in self.grammars:
            plt.figure()
            for iteration in self.results[grammar]:
                x = list(self.results[grammar][iteration].keys())
                y = list(self.results[grammar][iteration].values())
                plt.plot(x, y, label=f"Iterations: {iteration}")
            plt.xscale('log', base=2)
            plt.xlabel("Number of New Segments")
            plt.ylabel("Coverage (%)")
            plt.title(f"Coverage vs. New Segments for {os.path.basename(grammar)}")
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(self.output_dir, f"coverage_plot_{os.path.basename(grammar)}.png"))
            plt.close()
