## UParser: Unsupervised Morphological Segmentation

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


<br />
<div align="center">
  <a href="https://github.com/Netoamf/PIBIC-2023-24">
    <img src="images/logo2.png" alt="Logo" width="1000" height="300">  </a>

<h3 align="center">UParser</h3>

  <p align="center">
    Unsupervised morphological segmentation using BPE and MDL algorithms.
    <br />
    <a href="https://github.com/Netoamf/PIBIC-2023-24"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Netoamf/PIBIC-2023-24">View Demo</a>
    ·
    <a href="https://github.com/Netoamf/PIBIC-2023-24/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/Netoamf/PIBIC-2023-24/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#setting-up-the-virtual-environment">Setting up the Virtual Environment</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#arguments">Arguments</a></li>
    <li><a href="#example-usage">Example Usage</a></li>
    <li><a href="#morpheme-segmentation-with-bpe-and-mdl-in-uparser">Morpheme Segmentation with BPE and MDL in UParser</a></li>
    <li><a href="#disclaimer">Disclaimer</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
    <li><a href="#deprecated-versions">Deprecated Versions</a></li>
    <li><a href="#references">Bibliographic References</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

UParser is a tool designed for unsupervised morphological segmentation using the Byte Pair Encoding (BPE) and Minimum Description Length (MDL) algorithms. It offers a comprehensive approach to segmenting words into morphemes, providing insights into the underlying structure of languages.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* Python 3.6+
* [Matplotlib](https://matplotlib.org/)
* [ART](https://pypi.org/project/art/)
* [Pillow (PIL)](https://pillow.readthedocs.io/en/stable/)
* [Subword-nmt](https://github.com/rsennrich/subword-nmt)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

* Python 3.6 or higher
* pip (package installer for Python)

### Installation

1. Clone the repo:
   ```sh
   git clone https://github.com/Netoamf/PIBIC-2023-24.git
   ```

### Setting up the Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies for this project. Here's how to set it up:

1. **Navigate to the project directory:**
   ```bash
   cd UParser
   ```
2. **Create a virtual environment:**
   ```bash
   python -m venv .venv 
   ```
3. **Activate the virtual environment:**
   * **Windows:**
     ```bash
     .venv\Scripts\activate
     ```
   * **Linux/macOS:**
     ```bash
     source .venv/bin/activate
     ```
4. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

After setting up the environment, you can run UParser using the following command:

```bash
python main.py --folder <path_to_data_folder> --range <start_merge>-<end_merge> --output-dir <output_directory> --algorithm <BPE|MDL|Both>
```

### Arguments

* **`--folder` (required):** Path to the folder containing the text files.
* **`--range` (required for BPE):** Range of BPE merges (e.g., 0-10000).
* **`--step` (optional, default=100):** Interval between BPE merges.
* **`--verbose` (optional):** Enable detailed logs.
* **`--quiet` (optional):** Show only critical errors.
* **`--version` (optional):** Display UParser's version.
* **`--interactive` (optional):** Enable interactive mode.
* **`--dry-run` (optional):** Show operations without executing them.
* **`--output-dir` (optional, default='./output'):** Directory for generated files.
* **`--algorithm` (optional, default='BPE'):** Select the algorithm: BPE, MDL, or Both.

### Example Usage

To run BPE with merges from 0 to 10000 on the data in the `./data` folder and output results to `./results`:

```bash
python main.py --folder ./data --range 0-10000 --output-dir ./results
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MORPHEME SEGMENTATION WITH BPE AND MDL -->
## Morpheme Segmentation with BPE and MDL in UParser

UParser utilizes two distinct algorithms for unsupervised morpheme segmentation: Byte Pair Encoding (BPE) and Minimum Description Length (MDL).  Let's delve into how each of these algorithms operates within the context of UParser:

**Byte Pair Encoding (BPE)**

BPE is a data compression algorithm that iteratively merges the most frequent pair of consecutive bytes (or characters in our case) in a corpus. It starts with an initial vocabulary of individual characters and progressively merges pairs based on their frequency. This process continues until a predefined number of merges is reached or a desired vocabulary size is achieved.

**How BPE works in UParser:**

1. **Initialization:** The initial vocabulary consists of all unique characters present in the input corpus.
2. **Iteration:** In each iteration, the most frequent pair of consecutive characters is identified and merged into a new symbol. This new symbol is added to the vocabulary.
3. **Repetition:** Steps 2 and 3 are repeated until the desired number of merges is reached.
4. **Segmentation:** Once the merging process is complete, words are segmented by replacing the merged symbols with their corresponding character pairs.

**Minimum Description Length (MDL)**

MDL is a statistical framework based on information theory. It aims to find the best model that describes the data with the shortest possible code length. In the context of morpheme segmentation, MDL seeks the segmentation that minimizes the description length of the corpus, balancing the complexity of the lexicon (morpheme inventory) with the complexity of the segmented text.

**How MDL works in UParser:**

1. **Initialization:** The initial lexicon contains only individual characters.
2. **Analysis:** The algorithm analyzes the corpus and iteratively identifies potential new morphemes based on their frequency and contribution to minimizing the description length.
3. **Lexicon Update:** New morphemes are added to the lexicon if they improve the overall description length.
4. **Segmentation:** Words are segmented using the final lexicon, aiming for the segmentation that minimizes the description length.

**Key Differences:**

* **BPE** is primarily a data compression algorithm adapted for segmentation. It focuses on frequency and doesn't explicitly consider the linguistic notion of morphemes.
* **MDL** is a statistical framework that directly aims to find the most concise representation of the data, incorporating the concept of model complexity.

**UParser allows users to choose between BPE and MDL or compare their performance on the same dataset.** This provides flexibility and insights into the strengths and weaknesses of each algorithm for unsupervised morpheme segmentation.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- DISCLAIMER -->
## Disclaimer

For hardcore usage, use the following command:

```bash
python main.py --folder <path_to_data_folder> --range <start_merge>-<end_merge> --output-dir <output_directory> --algorithm <BPE|MDL|Both>
```

For a more straightforward and interactive experience, use:

```bash
python main.py --interactive
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

I would like to acknowledge the contributions of PIBIC, my project coleagues and my supervisor João Paulo Cyrino.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- OLD VERSIONS -->
## Deprecated Versions
This repository contains the deprecated (called Uchunker and BPE) but working versions of the algorithms. Uparser unifies into a new program and uses the subword-nmt library for BPE.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Bibliographic References
```bash
@inproceedings{sennrich-etal-2016-neural,
    title = "Neural Machine Translation of Rare Words with Subword Units",
    author = "Sennrich, Rico  and
      Haddow, Barry  and
      Birch, Alexandra",
    booktitle = "Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = aug,
    year = "2016",
    address = "Berlin, Germany",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P16-1162",
    doi = "10.18653/v1/P16-1162",
    pages = "1715--1725",
}

@article{RISSANEN1978465,
    title = {Modeling by shortest data description},
    journal = {Automatica},
    volume = {14},
    number = {5},
    pages = {465-471},
    year = {1978},
    issn = {0005-1098},
    doi = {https://doi.org/10.1016/0005-1098(78)90005-5},
    url = {https://www.sciencedirect.com/science/article/pii/0005109878900055},
    author = {J. Rissanen},
    keywords = {Modeling, parameter estimation, identification, statistics, stochastic systems},
    abstract = {The number of digits it takes to write down an observed sequence x1, …, xN of a time series depends on the model with its parameters that one assumes to have generated the observed data. Accordingly, by finding the model which minimizes the description length one obtains estimates of both the integer-valued structure parameters and the real-valued system parameters.}
}

@misc{demarcken1995unsupervisedacquisitionlexiconcontinuous,
  title={The Unsupervised Acquisition of a Lexicon from Continuous Speech}, 
  author={Carl de Marcken},
  year={1995},
  eprint={cmp-lg/9512002},
  archivePrefix={arXiv},
  primaryClass={cmp-lg},
  url={https://arxiv.org/abs/cmp-lg/9512002}, 
}

@article{10.1162/089120101750300490,
    author = {Goldsmith, John},
    title = "{Unsupervised Learning of the Morphology of a Natural Language}",
    journal = {Computational Linguistics},
    volume = {27},
    number = {2},
    pages = {153-198},
    year = {2001},
    month = {06},
    abstract = "{This study reports the results of using minimum description length (MDL) analysis to model unsupervised learning of the morphological segmentation of European languages, using corpora ranging in size from 5,000 words to 500,000 words. We develop a set of heuristics that rapidly develop a probabilistic morphological grammar, and use MDL as our primary tool to determine whether the modifications proposed by the heuristics will be adopted or not. The resulting grammar matches well the analysis that would be developed by a human morphologist.In the final section, we discuss the relationship of this style of MDL grammatical analysis to the notion of evaluation metric in early generative grammar.}",
    issn = {0891-2017},
    doi = {10.1162/089120101750300490},
    url = {https://doi.org/10.1162/089120101750300490},
    eprint = {https://direct.mit.edu/coli/article-pdf/27/2/153/1797583/089120101750300490.pdf},
}

```

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Netoamf/PIBIC-2023-24.svg?style=for-the-badge
[contributors-url]: https://github.com/Netoamf/PIBIC-2023-24/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Netoamf/PIBIC-2023-24.svg?style=for-the-badge
[forks-url]: https://github.com/Netoamf/PIBIC-2023-24/network/members
[stars-shield]: https://img.shields.io/github/stars/Netoamf/PIBIC-2023-24.svg?style=for-the-badge
[stars-url]: https://github.com/Netoamf/PIBIC-2023-24/stargazers
[issues-shield]: https://img.shields.io/github/issues/Netoamf/PIBIC-2023-24.svg?style=for-the-badge
[issues-url]: https://github.com/Netoamf/PIBIC-2023-24/issues
[license-shield]: https://img.shields.io/github/license/Netoamf/PIBIC-2023-24.svg?style=for-the-badge
[license-url]: https://github.com/Netoamf/PIBIC-2023-24/blob/master/LICENSE.txt


## PB



<h3 align="center">UParser</h3>

  <p align="center">
    Segmentação morfológica não supervisionada utilizando os algoritmos BPE e MDL.
    <br />
    <a href="https://github.com/Netoamf/PIBIC-2023-24"><strong>Explore a documentação »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Netoamf/PIBIC-2023-24">Ver Demonstração</a>
    ·
    <a href="https://github.com/Netoamf/PIBIC-2023-24/issues/new?labels=bug&template=bug-report---.md">Reportar Bug</a>
    ·
    <a href="https://github.com/Netoamf/PIBIC-2023-24/issues/new?labels=enhancement&template=feature-request---.md">Solicitar Funcionalidade</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Índice</summary>
  <ol>
    <li>
      <a href="#sobre-o-projeto">Sobre o Projeto</a>
      <ul>
        <li><a href="#construído-com">Construído com</a></li>
      </ul>
    </li>
    <li>
      <a href="#começando">Começando</a>
      <ul>
        <li><a href="#pré-requisitos">Pré-requisitos</a></li>
        <li><a href="#instalação">Instalação</a></li>
        <li><a href="#configurando-o-ambiente-virtual">Configurando o Ambiente Virtual</a></li>
      </ul>
    </li>
    <li><a href="#uso">Uso</a></li>
    <li><a href="#argumentos">Argumentos</a></li>
    <li><a href="#exemplo-de-uso">Exemplo de Uso</a></li>
    <li><a href="#segmentação-de-morfemas-com-bpe-e-mdl-no-uparser">Segmentação de Morfemas com BPE e MDL no UParser</a></li>
    <li><a href="#aviso">Aviso</a></li>
    <li><a href="#licença">Licença</a></li>
    <li><a href="#agradecimentos">Agradecimentos</a></li>
    <li><a href="#versões-anteriores">Versões Anteriores</a></li>
    <li><a href="#referências-bibliográficas">Referências Bibliográficas</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## Sobre o Projeto

O UParser é uma ferramenta desenvolvida para segmentação morfológica não supervisionada utilizando os algoritmos Byte Pair Encoding (BPE) e Minimum Description Length (MDL). Ele oferece uma abordagem abrangente para segmentar palavras em morfemas, fornecendo insights sobre a estrutura subjacente das línguas.

<p align="right">(<a href="#readme-top">voltar ao topo</a>)</p>



### Construído com

* Python 3.6+
* [Matplotlib](https://matplotlib.org/)
* [ART](https://pypi.org/project/art/)
* [Pillow (PIL)](https://pillow.readthedocs.io/en/stable/)
* [Subword-nmt](https://github.com/rsennrich/subword-nmt)


<p align="right">(<a href="#readme-top">voltar ao topo</a>)</p>



<!-- GETTING STARTED -->
## Começando

Para obter uma cópia local em funcionamento, siga estes simples passos de exemplo.

### Pré-requisitos

* Python 3.6 ou superior
* pip (instalador de pacotes para Python)

### Instalação

1. Clone o repositório:
   ```sh
   git clone https://github.com/Netoamf/PIBIC-2023-24.git
   ```

### Configurando o Ambiente Virtual

É altamente recomendável usar um ambiente virtual para gerenciar as dependências deste projeto. Veja como configurá-lo:

1. **Navegue até o diretório do projeto:**
   ```bash
   cd UParser
   ```
2. **Crie um ambiente virtual:**
   ```bash
   python -m venv .venv 
   ```
3. **Ative o ambiente virtual:**
   * **Windows:**
     ```bash
     .venv\Scripts\activate
     ```
   * **Linux/macOS:**
     ```bash
     source .venv/bin/activate
     ```
4. **Instale os pacotes necessários:**
   ```bash
   pip install -r requirements.txt
   ```

<p align="right">(<a href="#readme-top">voltar ao topo</a>)</p>



<!-- USAGE EXAMPLES -->
## Uso

Após configurar o ambiente, você pode executar o UParser usando o seguinte comando:

```bash
python main.py --folder <caminho_para_pasta_de_dados> --range <inicio_mesclagem>-<fim_mesclagem> --output-dir <diretorio_saida> --algorithm <BPE|MDL|Ambos>
```

### Argumentos

* **`--folder` (obrigatório):** Caminho para a pasta contendo os arquivos de texto.
* **`--range` (obrigatório para BPE):** Intervalo de mesclagens do BPE (ex: 0-10000).
* **`--step` (opcional, padrão=100):** Intervalo entre as mesclagens do BPE.
* **`--verbose` (opcional):** Habilita logs detalhados.
* **`--quiet` (opcional):** Mostra apenas erros críticos.
* **`--version` (opcional):** Exibe a versão do UParser.
* **`--interactive` (opcional):** Habilita o modo interativo.
* **`--dry-run` (opcional):** Mostra as operações sem executá-las.
* **`--output-dir` (opcional, padrão='./output'):** Diretório para os arquivos gerados.
* **`--algorithm` (opcional, padrão='BPE'):** Seleciona o algoritmo: BPE, MDL ou Ambos.

### Exemplo de Uso

Para executar o BPE com mesclagens de 0 a 10000 nos dados na pasta `./data` e gerar os resultados em `./results`:

```bash
python main.py --folder ./data --range 0-10000 --output-dir ./results
```

<p align="right">(<a href="#readme-top">voltar ao topo</a>)</p>


<!-- MORPHEME SEGMENTATION WITH BPE AND MDL -->
## Segmentação de Morfemas com BPE e MDL no UParser

O UParser utiliza dois algoritmos distintos para segmentação morfológica não supervisionada: Byte Pair Encoding (BPE) e Minimum Description Length (MDL). Vamos nos aprofundar em como cada um desses algoritmos opera dentro do contexto do UParser:

**Byte Pair Encoding (BPE)**

O BPE é um algoritmo de compressão de dados que mescla iterativamente o par mais frequente de bytes consecutivos (ou caracteres, no nosso caso) em um corpus. Ele começa com um vocabulário inicial de caracteres individuais e progressivamente mescla pares com base em sua frequência. Esse processo continua até que um número predefinido de mesclagens seja atingido ou um tamanho de vocabulário desejado seja alcançado.

**Como o BPE funciona no UParser:**

1. **Inicialização:** O vocabulário inicial consiste em todos os caracteres únicos presentes no corpus de entrada.
2. **Iteração:** Em cada iteração, o par mais frequente de caracteres consecutivos é identificado e mesclado em um novo símbolo. Esse novo símbolo é adicionado ao vocabulário.
3. **Repetição:** As etapas 2 e 3 são repetidas até que o número desejado de mesclagens seja atingido.
4. **Segmentação:** Uma vez que o processo de mesclagem esteja completo, as palavras são segmentadas substituindo os símbolos mesclados por seus pares de caracteres correspondentes.

**Minimum Description Length (MDL)**

O MDL é uma estrutura estatística baseada na teoria da informação. Ele visa encontrar o melhor modelo que descreve os dados com o menor comprimento de código possível. No contexto da segmentação de morfemas, o MDL busca a segmentação que minimiza o comprimento da descrição do corpus, equilibrando a complexidade do léxico (inventário de morfemas) com a complexidade do texto segmentado.

**Como o MDL funciona no UParser:**

1. **Inicialização:** O léxico inicial contém apenas caracteres individuais.
2. **Análise:** O algoritmo analisa o corpus e identifica iterativamente potenciais novos morfemas com base em sua frequência e contribuição para minimizar o comprimento da descrição.
3. **Atualização do Léxico:** Novos morfemas são adicionados ao léxico se eles melhorarem o comprimento geral da descrição.
4. **Segmentação:** As palavras são segmentadas usando o léxico final, visando a segmentação que minimiza o comprimento da descrição.

**Principais Diferenças:**

* **BPE:** É primariamente um algoritmo de compressão de dados adaptado para segmentação. Ele se concentra na frequência e não considera explicitamente a noção linguística de morfemas.
* **MDL:** É uma estrutura estatística que visa diretamente encontrar a representação mais concisa dos dados, incorporando o conceito de complexidade do modelo.

**O UParser permite que os usuários escolham entre BPE e MDL ou comparem seu desempenho no mesmo conjunto de dados.** Isso fornece flexibilidade e insights sobre os pontos fortes e fracos de cada algoritmo para a segmentação de morfemas não supervisionada.

<p align="right">(<a href="#readme-top">voltar ao topo</a>)</p>



<!-- DISCLAIMER -->
## Aviso

Para uso avançado, utilize o seguinte comando:

```bash
python main.py --folder <caminho_para_pasta_de_dados> --range <inicio_mesclagem>-<fim_mesclagem> --output-dir <diretorio_saida> --algorithm <BPE|MDL|Ambos>
```

Para uma experiência mais simples e interativa, utilize:

```bash
python main.py --interactive
```

<p align="right">(<a href="#readme-top">voltar ao topo</a>)</p>



<!-- LICENSE -->
## Licença

Distribuído sob a Licença MIT. Consulte `LICENSE.txt` para obter mais informações.

<p align="right">(<a href="#readme-top">voltar ao topo</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Agradecimentos

Gostaria de agradecer as contribuições do PIBIC, meus colegas de projeto e meu orientador João Paulo Cyrino.

<p align="right">(<a href="#readme-top">voltar ao topo</a>)</p>

<!-- OLD VERSIONS -->
## Versões Anteriores
Este repositório contém as versões antigas (chamadas de Uchunker e BPE), mas funcionais, dos algoritmos. O Uparser unifica em um novo programa e usa a biblioteca subword-nmt para o BPE.
<p align="right">(<a href="#readme-top">voltar ao topo</a>)</p>

## Referências Bibliográficas
```bash
@inproceedings{sennrich-etal-2016-neural,
    title = "Neural Machine Translation of Rare Words with Subword Units",
    author = "Sennrich, Rico  and
      Haddow, Barry  and
      Birch, Alexandra",
    booktitle = "Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = aug,
    year = "2016",
    address = "Berlin, Germany",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P16-1162",
    doi = "10.18653/v1/P16-1162",
    pages = "1715--1725",
}

@article{RISSANEN1978465,
    title = {Modeling by shortest data description},
    journal = {Automatica},
    volume = {14},
    number = {5},
    pages = {465-471},
    year = {1978},
    issn = {0005-1098},
    doi = {https://doi.org/10.1016/0005-1098(78)90005-5},
    url = {https://www.sciencedirect.com/science/article/pii/0005109878900055},
    author = {J. Rissanen},
    keywords = {Modeling, parameter estimation, identification, statistics, stochastic systems},
    abstract = {The number of digits it takes to write down an observed sequence x1, …, xN of a time series depends on the model with its parameters that one assumes to have generated the observed data. Accordingly, by finding the model which minimizes the description length one obtains estimates of both the integer-valued structure parameters and the real-valued system parameters.}
}

@misc{demarcken1995unsupervisedacquisitionlexiconcontinuous,
  title={The Unsupervised Acquisition of a Lexicon from Continuous Speech}, 
  author={Carl de Marcken},
  year={1995},
  eprint={cmp-lg/9512002},
  archivePrefix={arXiv},
  primaryClass={cmp-lg},
  url={https://arxiv.org/abs/cmp-lg/9512002}, 
}

@article{10.1162/089120101750300490,
    author = {Goldsmith, John},
    title = "{Unsupervised Learning of the Morphology of a Natural Language}",
    journal = {Computational Linguistics},
    volume = {27},
    number = {2},
    pages = {153-198},
    year = {2001},
    month = {06},
    abstract = "{This study reports the results of using minimum description length (MDL) analysis to model unsupervised learning of the morphological segmentation of European languages, using corpora ranging in size from 5,000 words to 500,000 words. We develop a set of heuristics that rapidly develop a probabilistic morphological grammar, and use MDL as our primary tool to determine whether the modifications proposed by the heuristics will be adopted or not. The resulting grammar matches well the analysis that would be developed by a human morphologist.In the final section, we discuss the relationship of this style of MDL grammatical analysis to the notion of evaluation metric in early generative grammar.}",
    issn = {0891-2017},
    doi = {10.1162/089120101750300490},
    url = {https://doi.org/10.1162/089120101750300490},
    eprint = {https://direct.mit.edu/coli/article-pdf/27/2/153/1797583/089120101750300490.pdf},
}

```
