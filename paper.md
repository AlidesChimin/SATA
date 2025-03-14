---
title: "ATAS - Academic Text Analysis System"
tags:
- NLP
- Content Analysis
- Humanities
- Text Analysis
- Geography
- Python
authors:
  - name: "Alides Baptista Chimin Junior"
    orcid: "0000-0002-7436-390X"
    affiliation: "1"
affiliations:
  - name: "Universidade Estadual do Centro-Oeste (UNICENTRO)"
    index: 1
date: 18 February 2025
bibliography: paper.bib
---


# Abstract

The **ATAS - Academic Text Analysis System** (Brazilian Portuguese SATA - Sistema de Análise de Textos Acadêmicos) is an open-source software developed to assist researchers in **textual content analysis**. Inspired by the methodology of **Laurence Bardin (2011)**, ATAS facilitates the **extraction, filtering, and statistical analysis** of academic texts, enabling the identification of semantic and linguistic patterns.

The software is particularly useful for researchers in the **Humanities and Social Sciences**, providing tools for analyzing **keywords, bigrams, lexical categories**, and other quantitative metrics of textual analysis. It integrates natural language processing (NLP) and allows data export to software such as **Gephi** for semantic network analysis.

We emphasize that the tools are in Portuguese, as they were developed by a Brazilian researcher and are being used by the GEPES and GETE research groups.

# Statement of Need

Academic text analysis is a **time-consuming and subjective** process, especially in qualitative research. ATAS automates part of this process, allowing researchers to:

- **Filter relevant terms** from large volumes of text.
- **Generate bigram tables** for semantic network analysis.
- **Classify the gender** of authors in textual datasets.
- **Perform textual statistics**, such as lexical diversity and sentiment analysis.

The intersection between discourse and spatiality can be analyzed through spatial statistics and semantic networks without necessarily relying on Geographic Information Systems (GIS). **Gilberto Câmara (2017)** critiques the limitations of GIS by arguing that its computational structure reduces complex geographic processes to discrete representations, oversimplifying spatial dynamics and ignoring the dialectics of geographic phenomena. ATAS emerges as a methodological alternative that enables the representation of discursive spatialities without the need for traditional cartography.

# Features and Usage

## 1. Text Filtering (Brazilian Portuguese: Filtragem de Texto)

Extracts **verbs, adjectives, and nouns** from texts, facilitating qualitative analyses.

- **Library used:** `spaCy`
- **How to use:**
  1. Open ATAS and go to the **Filter Text** option.
  2. Select the `.txt` file to be analyzed.
  3. The system processes the text and saves a new filtered file.

## 2. Table Conversion (Brazilian Portuguese: Conversão para Tabela)

Generates **bigrams** from the text and exports the data in **CSV** format, useful for analysis in **Gephi**.

- **Library used:** `pandas`
- **How to use:**
  1. Access the **Convert Text to Table** option.
  2. Choose a `.txt` file.
  3. ATAS generates a CSV file containing the bigrams, ready for network analysis.

## 3. Gender Identification (Brazilian Portuguese: Identificação de Gênero)

Automatically classifies the gender of proper names found in a textual dataset.

- **Library used:** `gender_guesser`
- **How to use:**
  1. Select the **Identify Gender** option.
  2. Upload a CSV file containing a list of names.
  3. ATAS generates a new CSV with the gender classification associated with each name.

## 4. Text Statistics (Brazilian Portuguese: Estatísticas de Texto)

Provides quantitative metrics such as **word frequency, named entities, lexical diversity, and sentiment analysis**.

- **Libraries used:** `TextBlob`, `spaCy`, `pandas`
- **How to use:**
  1. Go to the **Text Statistics** option.
  2. Select a text file.
  3. The system presents a detailed statistical report, including **word clouds and graphs**.

## 5. Graphical Interface

ATAS offers an intuitive visual interface based on `tkinter` and `ttkbootstrap`, allowing users without programming knowledge to easily access its functionalities.

# Implementation

ATAS is developed in **Python 3.8+** and utilizes:

- **`spaCy`** for text processing.
- **`pandas`** for data manipulation.
- **`tkinter`**\*\* and \*\***`ttkbootstrap`** for the graphical interface.
- **`TextBlob`** for sentiment analysis.
- **`gender_guesser`** for gender identification.

The source code is available on GitHub: [https://github.com/AlidesChimin/SATA](https://github.com/AlidesChimin/SATA)

# References

Refer to the `paper.bib` file for the complete list of references.

# Acknowledgments

I thank the project collaborators and the research groups **GEPES** and **GETE**, who influenced the conception of this software.

---

🔗 **Zenodo DOI**: [10.5281/zenodo.14868064](https://doi.org/10.5281/zenodo.14868064)


