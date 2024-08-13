import matplotlib.pyplot as plt
from math import log2
from menu import compare_segmentations_to_file
from process_descriptive_grammar import ProcessDescriptiveGrammar
from uchunker import UChunker

class Experiments:
    """
    This class executes experiments with the UChunker algorithm using different descriptive grammars,
    iterations, and numbers of new segments. It also plots the coverage results.
    """

    def __init__(self, grammars, max_iterations=16, max_segments=1024):
        """
        Initializes the Experiments object.

        :param grammars: A list of descriptive grammar file names.
        :param max_iterations: The maximum number of iterations (logarithmically spaced).
        :param max_segments: The maximum number of new segments (logarithmically spaced).
        """
        self.grammars = grammars
        self.max_iterations = max_iterations
        self.max_segments = max_segments
        self.results = {}

    def run_experiments(self):
        """
        Runs experiments for each grammar with varying iterations and new segments.
        """
        for grammar in self.grammars:
            print(f"Processing grammar: {grammar}")
            self.results[grammar] = {}

            # Criar arquivos de morfemas e segmentações
            output_morphemes = ProcessDescriptiveGrammar.extract_morphemes_from_file(grammar)
            output_segmentations = ProcessDescriptiveGrammar.words_from_file_regex(grammar)
            print(f"Morphemes file saved as: {output_morphemes}")
            print(f"Segmentations file saved as: {output_segmentations}")

            output_filename = f"compare_segmentations_{grammar}_results.txt"
            with open(output_filename, "w", encoding="utf-8") as output_file:
                for iteration in [2**i for i in range(int(log2(self.max_iterations)) + 1)]:
                    self.results[grammar][iteration] = {}
                    for n_segments in [2**j for j in range(int(log2(self.max_segments)) + 1)]:
                        print(f"Running experiment for grammar: {grammar}, iterations: {iteration}, new segments: {n_segments}")

                        # Criar uma nova instância do chunker a cada rodada de n_segments
                        chunker = UChunker(grammar)  
                        chunker.start(n_segments, iteration)

                        # Chamar compare_segmentations_to_file fora do bloco with open()
                        best_matches, total_morphemes = compare_segmentations_to_file(
                            chunker.lexicon, output_segmentations, output_filename  # Passar o nome do arquivo
                        )
                        coverage = (best_matches / total_morphemes) * 100
                        self.results[grammar][iteration][n_segments] = coverage
                        print(f"Coverage: {coverage:.2f}%")
                        output_file.write(f"Grammar: {grammar}, Iterations: {iteration}, New Segments: {n_segments}, Coverage: {coverage:.2f}%\n")

                        # Limpar a memória do chunker 
                        del chunker

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
            plt.title(f"Coverage vs. New Segments for {grammar}")
            plt.legend()
            plt.grid(True)
            plt.savefig(f"coverage_plot_{grammar}.png")

if __name__ == "__main__":
    grammars = ["bathari.txt", "daw.txt"] 
    experiments = Experiments(grammars)
    experiments.run_experiments()
    experiments.plot_results()