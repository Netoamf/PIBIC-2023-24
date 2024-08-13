from math import log2, inf
from collections import Counter
from utils import words_from_file, words_from_file_regex

class UChunker:
    def __init__(self, filename, analysis_output="analysis.txt", log_output="log.txt"):
        """
        Initializes the UChunker with the provided filename and output files.
        """
        # Utilize words_from_file from utils.py instead of ProcessDescriptiveGrammar
        self.corpus = words_from_file(filename, "corpus_temp.txt")
        self.char_set = set()
        self.lexicon = Counter()
        self.analysis_output = analysis_output
        self.log_output = log_output

        for line in self.corpus:
            chars = ''.join(line)
            for c in chars:
                self.lexicon[c] += 1
            self.char_set |= set(chars)
        
        self.char_cost = -1 * log2(1 / len(self.char_set))

    def start(self, n_new_segments, n_iterations):
        """
        Starts the chunker process with specified segments and iterations.
        """
        for i in range(n_iterations):
            first_parse = self.new_segments_from_parse()
            print(f"Iteração {i}")
            print(f"Custo atual do léxico: {self.lexicon_cost()}")
            print(f"Custo atual da análise: {first_parse[1]}")
            print(f"Custo da hipótese: {self.lexicon_cost() + first_parse[1]}")
            self.new_lexicon(first_parse[0], n_new_segments)

    def reset_lexicon(self):
        """Resets the lexicon to its initial state."""
        self.lexicon = Counter()
        for line in self.corpus:
            chars = ''.join(line)
            for c in chars:
                self.lexicon[c] += 1

    def new_segments_from_parse(self):
        """
        Parses the corpus to find new segments.
        :return: New segments and their parse cost.
        """
        new_segments = Counter()
        parse_cost = 0
        for line in self.corpus:
            analysis_cost, parse = self.analyse(line)
            parse_cost += analysis_cost
            for i in range(0, len(parse), 2):
                if i == len(parse) - 1:
                    new_segments[parse[i]] += 1
                else:
                    new_segments[parse[i] + parse[i + 1]] += 1
        return new_segments, parse_cost

    def new_lexicon(self, new_segments, n_new_segments):
        """
        Updates the lexicon with new segments.
        """
        new_segments_count = {}
        for segment, freq in new_segments.most_common(n_new_segments):
            new_segments_count[segment] = freq
        for segment, freq in new_segments_count.items():
            self.lexicon[segment] += freq
        with open(self.log_output, "w", encoding="UTF-8") as log_file:
            for segment, freq in self.lexicon.items():
                log_file.write(f"{segment}: {freq}\n")
        new_lexicon = Counter()
        for line in self.corpus:
            for segment in self.analyse(line)[1]:
                new_lexicon[segment] += 1
        self.lexicon = new_lexicon

    def item_cost(self, item):
        """
        Computes the cost of an item based on its probability in the lexicon.
        :param item: Item to compute the cost for.
        :return: Cost of the item.
        """
        prob = self.lexicon[item] / self.lexicon.total()
        if prob == 0:
            return inf
        return -1 * log2(prob)

    def analyse(self, char_sequence):
        """
        This method employs a forward-backward algorithm.
        The forward step computes the optimal segmentation and associated costs for each prefix of the sequence.
        The backward step traces back from the end of the sequence to find the actual segmentation that yields the minimum cost.

        :param char_sequence: Character sequence to analyze.
        :type char_sequence: str
        :return: Tuple containing the cost of the analysis and the list of segments.
        :rtype: Tuple[float, List[str]]
        """
        costs = [0]
        segments = []

        for final_position in range(1, len(char_sequence) + 1):
            candidates = dict()
            for initial_position in range(0, final_position):
                current_sequence = char_sequence[initial_position:final_position]
                candidates[current_sequence] = self.item_cost(current_sequence) + costs[initial_position]
            chosen = min(candidates, key=candidates.get)

            if candidates[chosen] == inf:
                chosen = char_sequence[final_position - 1]

            segments.append(chosen)
            costs.append(candidates[chosen])

        reversed_segments = list(reversed(segments))
        final_segments = []
        i = 0
        while i < len(reversed_segments):
            final_segments.append(reversed_segments[i])
            segment_length = len(reversed_segments[i])
            i += segment_length

        cost_of_analysis = sum(map(self.item_cost, final_segments))

        with open(self.analysis_output, "a", encoding="UTF-8") as analysis_file:
            analysis_file.write(f"Análise: {' '.join(final_segments)}\n")

        return cost_of_analysis, list(reversed(final_segments))

    def analysis_cost(self):
        """
        Computes the total cost of analysis.
        :return: Total analysis cost.
        """
        return sum(map(lambda x: self.analyse(x)[0], self.corpus))

    def lexicon_cost(self):
        """
        Computes the total cost of the lexicon.
        :return: Total lexicon cost.
        """
        return sum(map(lambda x: len(x) * self.char_cost, self.lexicon.keys()))

    def hypothesis_cost(self):
        """
        Computes the total hypothesis cost.
        :return: Total hypothesis cost.
        """
        return self.lexicon_cost() + self.analysis_cost()
