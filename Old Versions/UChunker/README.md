# UChunker

## (EN)
## Authorship and Affiliation

- **Authors:** Antonio Morais de Freitas Neto and Prof. João Paulo Lazzarini Cyrino
- **Affiliation:** Universidade Federal da Bahia

## Description

This project implements a Minimum Description Length (MDL) algorithm for morphological segmentation based on the algorithm proposed by Carl De Marcken. The goal is to segment a corpus into morphemes efficiently by minimizing the combined cost of encoding the lexicon and the corpus itself.

## Modules

The project is divided into several modules for better organization and maintainability:

1. **`process_descriptive_grammar.py`**: Contains the `ProcessDescriptiveGrammar` class which is responsible for extracting words and morphemes from a descriptive grammar file.
2. **`uchunker.py`**: Contains the `UChunker` class which handles the chunking and segmentation process using the MDL principle.
3. **`comparison.py`**: Provides functions to compare morphemes and segmentations against a lexicon and write the results to output files.
4. **`menu.py`**: Implements a menu-driven interface for users to interact with the different functionalities of the project.
5. **`main.py`**: The entry point of the application that runs the menu interface.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Netoamf/PIBIC-2023-24.git
   ```

## Usage

1. Run the main script:
    ```bash
    python main.py
    ```

** Follow the menu prompts to: 
- Process descriptive grammar.
- Start the chunker.
- Compare Morphemes.
- Compare Segmentations.

## Step-by-Step Instructions

1. Select **option 1** from the menu.
2. Enter the name of the file containing the descriptive grammar.
3. The program will generate files with morphemes and segmented words.
4. Start the chunker selecting **option 2**
5. Enter the name of the file containing the descriptive grammar.
6. Specify the number of new segments and the number of iterations.
7. The chunker will process the data and output the analysis results.
8. To Compare Morphemes Select **option 3** (Ensure the chunker has been started and the descriptive grammar has been processed.)
9. To Compare Segmentations Select **option 4** (Ensure the chunker has been started and the descriptive grammar has been processed.)
10. Select **option 5** to exit the program.

## Update!
This project has been enhanced with the capability to run automated experiments to analyze the UChunker algorithm's performance under various settings and datasets. The newly introduced `Experiments.py` module provides the following functionality:

**Key Features:**

- **Multiple Grammar Processing:**  Analyze UChunker's performance across different languages and grammatical structures by processing multiple descriptive grammar files.
- **Parameter Variation:** Conduct experiments with varying numbers of iterations and new segments, using logarithmic spacing to explore a wide range of possibilities.
- **Memory Management:** The chunker's memory is cleared after each round of experiments, ensuring independent results and preventing interference between different settings.
- **Detailed Reporting:** Gain insights into the algorithm's performance with comprehensive output files detailing segmentation coverage for each grammar, iteration, and segment count.
- **Graphical Visualization:** Visualize the relationship between coverage and the number of new segments through informative plots, making it easy to analyze the impact of different configurations on algorithm performance.

**How to Run Experiments:**

1. Navigate to the `UChunker` project directory.
2. Ensure your descriptive grammar files are in the same directory or provide the full path within the code.
3. Edit the `experiments.py` file and update the `grammars` variable with the list of grammar files you want to process:
   ```python
   if __name__ == "__main__":
       grammars = ["grammar1.txt", "grammar2.txt"]  # Replace with your grammar files
   ```
4. Execute the `experiments.py` script:
   ```bash
   python experiments.py
   ```
   The script will generate output files containing comparison results and coverage plots in the same directory.

   
## (PB)

## Autoria e Afiliação

- **Autores:** Antonio Morais de Freitas Neto e Prof. João Paulo Lazzarini Cyrino
- **Afiliação:** Universidade Federal da Bahia

## Descrição

Este projeto implementa um algoritmo de Comprimento Mínimo de Descrição (MDL) para segmentação morfológica baseado no algoritmo proposto por Carl De Marcken. O objetivo é segmentar um corpus em morfemas de forma eficiente, minimizando o custo combinado de codificação do léxico e do próprio corpus.

## Módulos

O projeto está dividido em vários módulos para melhor organização e manutenção:

1. **`process_descriptive_grammar.py`**: Contém a classe `ProcessDescriptiveGrammar`, responsável por extrair palavras e morfemas de um arquivo de gramática descritiva.
2. **`uchunker.py`**: Contém a classe `UChunker`, que lida com o processo de chunking e segmentação usando o princípio MDL.
3. **`comparison.py`**: Fornece funções para comparar morfemas e segmentações com um léxico e gravar os resultados em arquivos de saída.
4. **`menu.py`**: Implementa uma interface de menu para usuários interagirem com as diferentes funcionalidades do projeto.
5. **`main.py`**: O ponto de entrada da aplicação que executa a interface do menu.

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/Netoamf/PIBIC-2023-24.git
   ```

## Utilização

1. Execute o script principal:
   ```bash
   python main.py
   ```

**Siga as instruções do menu para:**
- Processar a gramática descritiva.
- Iniciar o chunker.
- Comparar Morfemas.
- Comparar Segmentações.

## Instruções Detalhadas

1. Selecione a **opção 1** no menu.
2. Digite o nome do arquivo que contém a gramática descritiva.
3. O programa irá gerar arquivos com morfemas e palavras segmentadas.
4. Inicie o chunker selecionando a **opção 2**.
5. Digite o nome do arquivo que contém a gramática descritiva.
6. Especifique o número de novos segmentos e o número de iterações.
7. O chunker irá processar os dados e exibir os resultados da análise.
8. Para comparar morfemas, selecione a **opção 3** (certifique-se de que o chunker foi iniciado e a gramática descritiva foi processada).
9. Para comparar segmentações, selecione a **opção 4** (certifique-se de que o chunker foi iniciado e a gramática descritiva foi processada).
10. Selecione a **opção 5** para sair do programa. 

##  Update!

Este projeto foi aprimorado com a capacidade de executar experimentos automatizados para analisar o desempenho do algoritmo UChunker sob diferentes configurações e conjuntos de dados. O novo módulo `Experiments.py` oferece as seguintes funcionalidades:

**Principais Recursos:**

- **Processamento de Múltiplas Gramáticas:** Analise o desempenho do UChunker em diversas línguas e estruturas gramaticais, processando múltiplos arquivos de gramática descritiva.
- **Variação de Parâmetros:**  Execute experimentos com diferentes números de iterações e quantidades de novos segmentos, utilizando um espaçamento logarítmico para explorar um amplo espectro de possibilidades.
- **Gerenciamento de Memória:**  A memória utilizada pelo chunker é limpa após cada rodada de experimentos, garantindo resultados independentes e evitando interferências entre diferentes configurações.
- **Relatórios Detalhados:**  Obtenha insights sobre o desempenho do algoritmo com arquivos de saída abrangentes, que detalham a cobertura da segmentação para cada gramática, iteração e número de segmentos.
- **Visualização Gráfica:** Visualize a relação entre a cobertura e o número de novos segmentos através de gráficos informativos, que facilitam a análise do impacto das diferentes configurações no desempenho do algoritmo.

**Como Executar Experimentos:**

1. Navegue até o diretório do projeto `UChunker`.
2. Certifique-se de que seus arquivos de gramática descritiva estejam no mesmo diretório ou forneça o caminho completo no código.
3. Edite o arquivo `experiments.py` e atualize a variável `grammars` com a lista de arquivos de gramática que você deseja processar:
   ```python
   if __name__ == "__main__":
       grammars = ["grammar1.txt", "grammar2.txt"]  
   ```
4. Execute o script `experiments.py`:
   ```bash
   python experiments.py
   ```
   O script gerará arquivos de saída com os resultados das comparações e gráficos de cobertura no mesmo diretório.
