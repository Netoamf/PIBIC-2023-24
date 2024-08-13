import os
import argparse
import logging
from utils import create_directories, words_from_file, words_from_file_regex, calculate_frequencies
from preprocessing import preprocess_corpus
from segmentation import train_bpe, apply_bpe, compare_segments, save_correct_segmentations
from analysis import calculate_coverage, calculate_compression_ratio
from visualization import plot_coverage_vs_merges, plot_compression_vs_coverage, plot_frequent_segments_vs_merges
from uchunker import UChunker
from experiments import Experiments
from art import text2art
from collections import Counter 
import matplotlib.pyplot as plt  
from pic import print_centered_ascii_art, print_centered_text_art

def main():
    
    print_centered_ascii_art("pic.jpg", new_width=55, contrast_factor=1.0)
    print_centered_text_art("Welcome to UParser", font="tarty1")
    print_centered_text_art("Authorship: Antonio Morais e Joao Paulo Cyrino \n Institution: Universidade Federal da Bahia", font="tiny2")

    # Argument parser setup
    parser = argparse.ArgumentParser(
        description="UParser: Unsupervised morphological segmentation using BPE and MDL algorithms.",
        epilog="Example usage:\n  python uparser.py --folder ./data --range 0-10000 --output-dir ./results"
    )
    
    # Language selection
    #parser.add_argument('--lang', type=str, choices=['EN', 'PT'], default='EN', help="Select language: EN or PT.")
    
    # General options
    parser.add_argument('--folder', type=str, help="Path to the folder containing the text files.")
    parser.add_argument('--range', type=str, help="Range of BPE merges (e.g., 0-10000).")
    parser.add_argument('--step', type=int, default=100, help="Interval between BPE merges.")
    parser.add_argument('--verbose', action='store_true', help="Enable detailed logs.")
    parser.add_argument('--quiet', action='store_true', help="Show only critical errors.")
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('--interactive', action='store_true', help="Enable interactive mode.")
    parser.add_argument('--dry-run', action='store_true', help="Show the operations that would be performed without executing them.")
    parser.add_argument('--output-dir', type=str, help="Directory for generated files. Press Enter to use the default './output'.")
    parser.add_argument('--algorithm', type=str, choices=['BPE', 'MDL', 'Both'], help="Select the algorithm: BPE, MDL, or Both.")
    
    args = parser.parse_args()

    
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    elif args.quiet:
        logging.basicConfig(level=logging.ERROR)
    else:
        logging.basicConfig(level=logging.INFO)

    
    if not args.output_dir:
        args.output_dir = './output'
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # Interactive mode setup
    if args.interactive:
        if not args.folder:
            args.folder = input("Enter the path to the folder containing the text files: ")
        if not args.algorithm:
            args.algorithm = input("Select the algorithm (BPE, MDL, or Both): ")
        if args.algorithm in ['BPE', 'Both'] and not args.range:
            args.range = input("Enter the range of BPE merges (e.g., 0-10000): ")
        if not args.step:
            args.step = int(input("Enter the interval between BPE merges: "))
        if not args.output_dir:
            args.output_dir = input("Enter the output directory (press Enter to use './output'): ")
            if not args.output_dir:
                args.output_dir = './output'

    
    if not args.folder:
        raise ValueError("The --folder argument is required.")
    if args.algorithm in ['BPE', 'Both'] and not args.range:
        raise ValueError("The --range argument is required for BPE.")
    if not os.path.exists(args.folder):
        raise ValueError(f"The folder {args.folder} does not exist.")
    
    # Dry-run mode
    if args.dry_run:
        logging.info("Simulation mode activated. No operations will be performed.")
        logging.info(f"Output directory: {args.output_dir}")
        logging.info(f"Files to be processed: {os.listdir(args.folder)}")
        return
    
    # Initialize results storage
    bpe_results, mdl_results = None, None

    # Run BPE Algorithm
    if args.algorithm in ['BPE', 'Both']:
        logging.info("Running BPE algorithm...")
        bpe_results = run_bpe(args.folder, args.range, args.step, args.output_dir)
        logging.info("BPE algorithm completed.")

    # Run MDL Algorithm
    if args.algorithm in ['MDL', 'Both']:
        logging.info("Running MDL algorithm...")
        mdl_results = run_mdl(args.folder, args.output_dir)
        logging.info("MDL algorithm completed.")

    # Compare results if both algorithms are selected
    if args.algorithm == 'Both':
        if bpe_results is not None and mdl_results is not None:
            compare_algorithms(bpe_results, mdl_results, args.output_dir)
        else:
            logging.warning("One or both algorithm results are None, skipping comparison.")

def run_bpe(folder_path, range_of_merges, step, output_dir):
    init, final = map(int, range_of_merges.split('-'))
    bpe_results = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            language = os.path.splitext(filename)[0]
            base_path = create_directories(language)

            corpus_path = os.path.join(base_path, "corpus.txt")
            segmented_path = os.path.join(base_path, "corpus_segmented.txt")

            words = words_from_file(file_path, corpus_path)
            words_from_file_regex(file_path, segmented_path)

            original_vocab = Counter(words)
            initial_vocab_size = len(original_vocab)
            logging.info(f"Initial vocabulary size for {language}: {initial_vocab_size}")

            coverage_data = []
            compression_data = []
            segment_data = []

            for i in range(init, final + 1, step):
                preprocess_corpus(corpus_path)
                bpe_operations_path = os.path.join(base_path, "bpe_operations", f'bpe_operations_{i}_{language}.txt')
                if not train_bpe(corpus_path, bpe_operations_path, i):
                    continue

                output_segmented_corpus_path = os.path.join(base_path, "segmented_corpus", f'segmented_corpus_{i}_{language}.txt')
                if not apply_bpe(corpus_path, bpe_operations_path, output_segmented_corpus_path, i):
                    continue

                freqs = calculate_frequencies(output_segmented_corpus_path)
                final_vocab_size = len(freqs)
                logging.info(f"BPE merge operations: {i}")
                logging.info(f"Final vocabulary size: {final_vocab_size}")

                with open(f'{output_segmented_corpus_path}.freqs.txt', 'w', encoding='UTF-8') as freq_file:
                    for word, count in freqs.items():
                        freq_file.write(f'{word} {count}\n')

                with open(output_segmented_corpus_path, 'r', encoding='UTF-8') as file:
                    content = file.read().replace('@@ ', ' ')
                with open(output_segmented_corpus_path, 'w', encoding='UTF-8') as file:
                    file.write(content)

                with open(segmented_path, 'r', encoding='UTF-8') as file:
                    segmented_words = file.readlines()
                with open(output_segmented_corpus_path, 'r', encoding='UTF-8') as file:
                    bpe_segments = file.readlines()

                correct_segmentations = compare_segments(bpe_segments, segmented_words)
                coverage = calculate_coverage(bpe_segments, segmented_words)
                compression = calculate_compression_ratio(initial_vocab_size, final_vocab_size)
                
                correct_segmentations_path = os.path.join(base_path, "correct_segmentations", f'correct_segmentations_{i}_{language}.txt')
                save_correct_segmentations(correct_segmentations, correct_segmentations_path)

                logging.info(f'Coverage: {coverage:.2f}%')
                logging.info(f'Compression: {compression:.2f}%')
                logging.info(f'Correct segmentations saved to {correct_segmentations_path}')

                coverage_data.append((i, coverage))
                compression_data.append((compression, coverage))
                segment_data.extend([(word, i) for word, count in freqs.most_common(10)])

            plot_coverage_vs_merges(coverage_data, language)
            plot_compression_vs_coverage(compression_data, language)
            plot_frequent_segments_vs_merges(segment_data, language)

            report_path = os.path.join(output_dir, f'{language}_bpe_report.txt')
            with open(report_path, 'w', encoding='UTF-8') as report_file:
                report_file.write("Relatório de Segmentação Morfológica usando BPE\n")
                report_file.write(f"Linguagem: {language}\n")
                report_file.write(f"Intervalo de merges: {init}-{final}\n")
                report_file.write(f"Diretório de saída: {output_dir}\n")
                report_file.write("Coberturas:\n")
                for merge, coverage in coverage_data:
                    report_file.write(f"{merge} merges: {coverage:.2f}% cobertura\n")
            logging.info(f'Relatório BPE salvo em {report_path}')

            # Store the coverage data in memory
            if language not in bpe_results:
                bpe_results[language] = {}
            bpe_results[language][i] = coverage
    return bpe_results

def run_mdl(folder_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    mdl_results = {}
    grammars = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".txt")]
    
    if not grammars:
        logging.info("No grammar files found in the specified folder for MDL.")
        return mdl_results  # Return an empty dictionary if no grammar files are found

    experiments = Experiments(grammars, output_dir=output_dir)
    
    # Run experiments on all grammars at once
    mdl_results = experiments.run_experiments()
    
    
    logging.debug(f"MDL results structure: {type(mdl_results)}")
    logging.debug(f"MDL results content: {mdl_results}")

    
    if not isinstance(mdl_results, dict):
        logging.error("MDL results are not a dictionary. Returning an empty dictionary.")
        return {}

    
    if not mdl_results:
        logging.error("MDL results dictionary is empty.")
        return {}

    
    experiments.plot_results()
    
    logging.info("Experimentos com MDL concluídos.")
    return mdl_results



def compare_algorithms(bpe_results, mdl_results, output_dir):
    """
    Compare the results between BPE and MDL algorithms and generate comparison plots.
    """
    logging.info("Iniciando a comparação entre BPE e MDL...")

    # Criar o diretório de saída, se não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterar sobre cada língua presente nos resultados do BPE
    for lang in bpe_results:
        # Encontrar a chave em mdl_results que corresponde à língua atual
        mdl_key = None
        for key in mdl_results:
            if lang.lower() in key.lower():  # Comparação sem distinção entre maiúsculas e minúsculas
                mdl_key = key
                break

        if mdl_key:
            # Obter a cobertura máxima para BPE
            max_bpe_coverage = max(bpe_results[lang].values())

            # Obter a cobertura máxima para MDL (considerando todas as iterações e novos segmentos)
            max_mdl_coverage = 0
            for iterations in mdl_results[mdl_key].values():
                for coverage in iterations.values():
                    max_mdl_coverage = max(max_mdl_coverage, coverage)

            
            plt.figure(figsize=(8, 5))
            algorithms = ['BPE', 'MDL']
            coverages = [max_bpe_coverage, max_mdl_coverage]
            plt.bar(algorithms, coverages, color=['blue', 'green'])
            plt.ylim(0, 100)  
            plt.title(f'Cobertura para {lang}')
            plt.xlabel('Algoritmo')
            plt.ylabel('Cobertura (%)')
            plot_path = os.path.join(output_dir, f'coverage_comparison_{lang}.png')
            plt.tight_layout()
            plt.savefig(plot_path)
            plt.close()

            logging.info(f"Gráfico de comparação salvo para {lang} em {plot_path}")
        else:
            logging.warning(f"Resultados para {lang} não encontrados nos resultados do MDL.")

    logging.info("Comparação entre BPE e MDL concluída.")


if __name__ == "__main__":
    main()
