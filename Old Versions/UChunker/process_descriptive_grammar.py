from collections import Counter
import re

class ProcessDescriptiveGrammar:
    def __init__(self, filename):
        """
        Initializes the ProcessDescriptiveGrammar with the provided filename.
        """
        self.filename = filename

    def words_from_descriptive_grammar(self):
        """
        Extracts words from a descriptive grammar file.
        :return: List of words.
        """
        words = []
        with open(self.filename, "r", encoding="UTF-8") as file:
            lines = file.readlines()
        for i in range(0, len(lines), 3):
            phrase = lines[i].strip().replace('-', '').split()
            words.extend(phrase)
        return words

    @staticmethod
    def extract_morphemes_from_file(input_filename, output_filename="morphemes.txt"):
        """
        Extracts morphemes from a file and writes them to another file.
        :param input_filename: Input file name.
        :param output_filename: Output file name.
        :return: Output file name.
        """
        with open(input_filename, "r", encoding="UTF-8") as file:
            lines = file.readlines()
        with open(output_filename, "w", encoding="UTF-8") as output_file:
            for i in range(0, len(lines), 3):
                phrase = lines[i].strip()
                words = re.sub(r"-", " ", phrase).split()
                for word in words:
                    output_file.write(f"{word}\n")
        return output_filename
    
    @staticmethod
    def words_from_file_regex(filename, output_filename="corpus_segmented.txt"):
        """
        Extracts words from a file using regex and writes them to another file.
        :param filename: Input file name.
        :param output_filename: Output file name.
        :return: Output file name.
        """
        with open(filename, "r", encoding="UTF-8") as file:
            lines = file.readlines()
        with open(output_filename, "w", encoding="UTF-8") as output_file:
            for i in range(0, len(lines), 3):
                phrase = lines[i].strip()
                for word in re.findall(r"\S+", phrase):
                    word_without_hyphen = word.replace("-", " ") 
                    output_file.write(f"{word_without_hyphen}\n")
        return output_filename
