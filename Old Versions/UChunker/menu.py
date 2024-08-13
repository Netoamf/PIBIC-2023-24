from uchunker import UChunker
from process_descriptive_grammar import ProcessDescriptiveGrammar
from comparison import compare_morphemes_to_file, compare_segmentations_to_file

class Menu:
    def __init__(self):
        self.chunker = None
        self.output_morphemes = None
        self.output_segmentations = None

    def display_menu(self):
        """
        Displays the main menu options.
        """
        print("Selecione uma opção:")
        print("1. Processar gramática descritiva")
        print("2. Iniciar o chunker")
        print("3. Comparar morfemas")
        print("4. Comparar segmentações")
        print("5. Sair")

    def process_grammar(self):
        """
        Processes the descriptive grammar file.
        """
        filename = input("Digite o nome do arquivo da gramática descritiva: ")
        self.output_morphemes = ProcessDescriptiveGrammar.extract_morphemes_from_file(filename)
        self.output_segmentations = ProcessDescriptiveGrammar.words_from_file_regex(filename)
        print(f"Arquivo de morfemas salvo como: {self.output_morphemes}")
        print(f"Arquivo de segmentações salvo como: {self.output_segmentations}")

    def start_chunker(self):
        """
        Starts the chunker process.
        """
        if self.chunker is None:
            filename = input("Digite o nome do arquivo com a gramática descritiva: ")
            self.chunker = UChunker(filename)
        n_new_segments = int(input("Digite o número de novos segmentos: "))
        n_iterations = int(input("Digite o número de iterações: "))
        self.chunker.start(n_new_segments, n_iterations)
        print("Chunker iniciado e finalizado com sucesso!")

    def compare_morphemes(self):
        """
        Compares morphemes of the language to the inventory of morphemes created by the algorithm.
        """
        if self.chunker is None:
            print("Inicie o chunker antes de comparar morfemas.")
            return
        if self.output_morphemes is None:
            print("Processar a gramática descritiva primeiro.")
            return
        output_filename = "compare_morphemes_output.txt"
        best_matches_found, total_morphemes = compare_morphemes_to_file(self.chunker.lexicon, self.output_morphemes, output_filename)
        coverage = (best_matches_found / total_morphemes) * 100
        print(f"Resultado salvo em {output_filename}")
        print(f"A cobertura do inventário dos morfemas da língua foi de: {coverage:.2f}%")

    def compare_segmentations(self):
        """
        Compares segmentations from the descriptive grammar to the segments found by the algorithm.
        """
        if self.chunker is None:
            print("Inicie o chunker antes de comparar segmentações.")
            return
        if self.output_segmentations is None:
            print("Processar a gramática descritiva primeiro.")
            return
        output_filename = "compare_segmentations_output.txt"
        best_matches_found, total_morphemes = compare_segmentations_to_file(self.chunker.lexicon, self.output_segmentations, output_filename)
        coverage = (best_matches_found / total_morphemes) * 100
        print(f"Resultado salvo em {output_filename}")
        print(f"A cobertura das segmentações corretas foi de: {coverage:.2f}%")

    def run(self):
        """
        Runs the main menu loop.
        """
        while True:
            self.display_menu()
            choice = input("Escolha uma opção: ")
            if choice == "1":
                self.process_grammar()
            elif choice == "2":
                self.start_chunker()
            elif choice == "3":
                self.compare_morphemes()
            elif choice == "4":
                self.compare_segmentations()
            elif choice == "5":
                print("Saindo do programa.")
                break
            else:
                print("Opção inválida. Tente novamente.")
