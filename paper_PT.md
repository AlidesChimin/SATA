---
title: "SATA - Sistema de Análise de Textos Acadêmicos"
tags:
  - NLP
  - Análise de Conteúdo
  - Ciências Humanas
  - Análise de Texto
  - Geografia
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

# Resumo
O **SATA - Sistema de Análise de Textos Acadêmicos** é um software open-source desenvolvido para auxiliar pesquisadores na **análise de conteúdo textual**. Inspirado na metodologia de **Laurence Bardin (2011)**, o SATA facilita a **extração, filtragem e estatística** de textos acadêmicos, permitindo a identificação de padrões semânticos e linguísticos.

O software é especialmente útil para pesquisadores das **Ciências Humanas e Sociais**, fornecendo ferramentas para análise de **palavras-chave, bigramas, categorias lexicais** e outras métricas quantitativas de análise textual. Ele integra processamento de linguagem natural (NLP) e exportação de dados para softwares como **Gephi** para análise de redes semânticas.


# Statement of Need
A análise de textos acadêmicos é um processo **demorado e subjetivo**, especialmente em pesquisas qualitativas. O SATA automatiza parte desse processo, permitindo que pesquisadores:

- **Filtram termos** relevantes de grandes volumes de textos.
- **Gerem tabelas de bigramas** para análise em redes semânticas.
- **Classifiquem o gênero** de autores em conjuntos de dados textuais.
- **Realizem estatísticas textuais**, como diversidade lexical e análise de sentimentos.

A interseção entre discurso e espacialidade pode ser analisada por meio de estatísticas espaciais e redes semânticas, sem necessariamente depender de Sistemas de Informação Geográfica (SIG). **Gilberto Câmara (2017)** critica os limites dos SIGs ao argumentar que sua estrutura computacional reduz processos geográficos complexos a representações discretas, simplificando dinâmicas espaciais e ignorando a dialética dos fenômenos geográficos. O SATA surge como uma alternativa metodológica que permite representar espacialidades discursivas sem a necessidade de cartografia tradicional.

# Funcionalidades e Uso

## 1. Filtragem de Texto
Permite extrair **verbos, adjetivos e substantivos** de textos, facilitando análises qualitativas.
- **Biblioteca utilizada:** `spaCy`
- **Como usar:**
  1. Abra o SATA e vá até a opção **Filtrar Texto**.
  2. Selecione o arquivo `.txt` a ser analisado.
  3. O sistema processará o texto e salvará um novo arquivo filtrado.

## 2. Conversão para Tabela
Gera **bigramas** a partir do texto e exporta os dados em formato **CSV**, útil para análise em **Gephi**.
- **Biblioteca utilizada:** `pandas`
- **Como usar:**
  1. Acesse a opção **Converter Texto para Tabela**.
  2. Escolha um arquivo `.txt`.
  3. O SATA gerará um arquivo CSV contendo os bigramas, pronto para análise de redes.

## 3. Identificação de Gênero
Classifica automaticamente o gênero de nomes próprios encontrados em um conjunto de dados textuais.
- **Biblioteca utilizada:** `gender_guesser`
- **Como usar:**
  1. Selecione a opção **Identificar Gênero**.
  2. Carregue um arquivo CSV contendo uma lista de nomes.
  3. O SATA gerará um novo CSV com a classificação de gênero associada a cada nome.

## 4. Estatísticas de Texto
Fornece métricas quantitativas, como **frequência de palavras, entidades nomeadas, diversidade lexical e análise de sentimentos**.
- **Bibliotecas utilizadas:** `TextBlob`, `spaCy`, `pandas`
- **Como usar:**
  1. Vá até a opção **Estatísticas de Texto**.
  2. Selecione um arquivo de texto.
  3. O sistema apresentará um relatório estatístico detalhado, incluindo **nuvens de palavras e gráficos**.

## 5. Interface Gráfica
O SATA oferece uma interface visual intuitiva baseada em `tkinter` e `ttkbootstrap`, permitindo que usuários sem conhecimento em programação utilizem suas funcionalidades facilmente.

# Implementação
O SATA é desenvolvido em **Python 3.8+** e utiliza:
- **`spaCy`** para processamento de texto.
- **`pandas`** para manipulação de dados.
- **`tkinter` e `ttkbootstrap`** para a interface gráfica.
- **`TextBlob`** para análise de sentimentos.
- **`gender_guesser`** para identificação de gênero.

O código-fonte está disponível no GitHub: [https://github.com/AlidesChimin/SATA](https://github.com/AlidesChimin/SATA)

# Referências
Consulte o arquivo `paper.bib` para a lista completa de referências.

# Agradecimentos
Agradeço aos colaboradores do projeto e aos grupos de pesquisa **GEPES** e **GETE**, que influenciaram a concepção deste software.

---
🔗 **DOI do Zenodo**: [10.5281/zenodo.14868064](https://doi.org/10.5281/zenodo.14868064)


