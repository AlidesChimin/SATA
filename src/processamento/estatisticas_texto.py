# processamento/estatisticas_texto.py
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import spacy
import csv
import gender_guesser.detector as gender
from collections import Counter
import os

# Para análise de sentimento
from textblob import TextBlob

# Para gerar nuvens de palavras
from wordcloud import WordCloud

nlp = spacy.load('pt_core_news_sm')

def gerar_wordcloud(tokens, output_path):
    """
    Gera um arquivo .png contendo a nuvem de palavras
    a partir de uma lista de strings (tokens).
    Ignora se a lista estiver vazia.
    """
    text = " ".join(tokens)
    if not text.strip():
        return  # Não cria arquivo se não há tokens
    wc = WordCloud(width=800, height=400, background_color="white")
    wc.generate(text)
    wc.to_file(output_path)

def estatisticas_texto(janela_pai):
    """
    Lê um arquivo .txt, realiza múltiplas análises (classes gramaticais, 
    entidades, gênero, sentimento, etc.), salva resultados em CSV
    e gera nuvens de palavras e TAMBÉM salva análise de sentimentos e LOC em tabelas separadas.
    """
    arquivo_entrada = filedialog.askopenfilename(
        title="Selecione o arquivo TXT",
        filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
    )
    if arquivo_entrada:
        try:
            # 1. Lê o texto
            with open(arquivo_entrada, 'r', encoding='utf-8') as f:
                texto = f.read()
            doc = nlp(texto)

            # 2. Classes gramaticais
            verbs = [token for token in doc if token.pos_ == 'VERB']
            adjs = [token for token in doc if token.pos_ == 'ADJ']
            nouns = [token for token in doc if token.pos_ == 'NOUN']
            advs = [token for token in doc if token.pos_ == 'ADV']

            # 3. Entidades
            pessoas = [ent for ent in doc.ents if ent.label_ == 'PER']
            locs = [ent for ent in doc.ents if ent.label_ == 'LOC']
            orgs = [ent for ent in doc.ents if ent.label_ == 'ORG']

            # 4. Gênero (para pessoas)
            detector = gender.Detector()
            pessoas_sexo = [(p.text, detector.get_gender(str(p.text).split()[0])) for p in pessoas]
            homens = sum(1 for _, s in pessoas_sexo if s in ('male', 'mostly_male'))
            mulheres = sum(1 for _, s in pessoas_sexo if s in ('female', 'mostly_female'))

            # 5. Sentenças
            sents = list(doc.sents)
            num_sents = len(sents)
            avg_sent_length = sum(len(sent) for sent in sents)/num_sents if num_sents > 0 else 0

            # 6. Stopwords, Tokens e TTR
            stopwords_count = sum(1 for token in doc if token.is_stop)
            total_tokens = len(doc)
            unique_tokens = len({t.lemma_.lower() for t in doc if t.is_alpha})
            ttr = unique_tokens / total_tokens if total_tokens > 0 else 0

            # 7. Análise de Sentimento (TextBlob) – geral e por sentença
            blob = TextBlob(texto)
            sent_polarity = blob.sentiment.polarity
            sent_subjectivity = blob.sentiment.subjectivity

            # 7.1 Análise por frase (opcional):
            # Cria uma lista (sentimento_sentence) com tuplas do tipo (i, frase, polarity, subjectivity)
            sentimento_sentence = []
            for i, sent in enumerate(sents, start=1):
                tb = TextBlob(sent.text)
                sentimento_sentence.append((
                    i,
                    sent.text.strip(),
                    tb.sentiment.polarity,
                    tb.sentiment.subjectivity
                ))

            # 8. Arquivo principal CSV
            full_path = filedialog.asksaveasfilename(
                title="Selecione a pasta e o nome do arquivo para salvar (CSV principal)",
                defaultextension=".csv",
                filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")]
            )
            if full_path:
                # Salva métricas gerais no CSV principal
                with open(full_path, 'w', encoding='utf-8', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Categoria", "Valor"])
                    writer.writerow(["Verbos", len(verbs)])
                    writer.writerow(["Adjetivos", len(adjs)])
                    writer.writerow(["Substantivos (NOUN)", len(nouns)])
                    writer.writerow(["Advérbios (ADV)", len(advs)])
                    writer.writerow(["Homens (PER)", homens])
                    writer.writerow(["Mulheres (PER)", mulheres])
                    writer.writerow(["LOC (Locais)", len(locs)])
                    writer.writerow(["ORG (Organizações)", len(orgs)])
                    writer.writerow(["Número de sentenças", num_sents])
                    writer.writerow(["Comprimento médio das sentenças (tokens)", avg_sent_length])
                    writer.writerow(["Stopwords", stopwords_count])
                    writer.writerow(["Total de tokens", total_tokens])
                    writer.writerow(["Diversidade Lexical (TTR)", ttr])
                    writer.writerow(["Polaridade (Sentimento) [geral]", sent_polarity])
                    writer.writerow(["Subjetividade (Sentimento) [geral]", sent_subjectivity])

                # 8.1 Nomes base para arquivos extras
                base_filename = os.path.splitext(os.path.basename(full_path))[0]
                output_dir = os.path.dirname(full_path)

                # 9. Salvar análise de sentimento por sentença em CSV separado
                sentimento_csv_path = os.path.join(output_dir, f"{base_filename}_sentimento.csv")
                with open(sentimento_csv_path, 'w', encoding='utf-8', newline='') as sent_csv:
                    writer = csv.writer(sent_csv)
                    writer.writerow(["#Sentença", "Texto da Sentença", "Polaridade", "Subjetividade"])
                    for (i_sent, sent_text, pol, subj) in sentimento_sentence:
                        writer.writerow([i_sent, sent_text, pol, subj])

                # 10. Salvar lista de Locais em CSV separado (com contagem de frequência)
                locais_csv_path = os.path.join(output_dir, f"{base_filename}_locais.csv")
                loc_counter = Counter(ent.text.lower() for ent in locs)
                with open(locais_csv_path, 'w', encoding='utf-8', newline='') as loc_csv:
                    writer = csv.writer(loc_csv)
                    writer.writerow(["Local", "Frequência"])
                    for loc, freq in loc_counter.most_common():
                        writer.writerow([loc, freq])

                # 11. Geração das nuvens de palavras
                def nuvem_filepath(sufixo):
                    return os.path.join(output_dir, f"{base_filename}_nuvem_{sufixo}.png")

                # WordCloud de verbos
                verbos_text = [token.lemma_.lower() for token in verbs if token.is_alpha]
                gerar_wordcloud(verbos_text, nuvem_filepath("verbos"))

                # WordCloud de substantivos
                nouns_text = [token.lemma_.lower() for token in nouns if token.is_alpha]
                gerar_wordcloud(nouns_text, nuvem_filepath("substantivos"))

                # WordCloud de adjetivos
                adjs_text = [token.lemma_.lower() for token in adjs if token.is_alpha]
                gerar_wordcloud(adjs_text, nuvem_filepath("adjetivos"))

                # WordCloud de advérbios
                advs_text = [token.lemma_.lower() for token in advs if token.is_alpha]
                gerar_wordcloud(advs_text, nuvem_filepath("adverbios"))

                # WordCloud de Locais (LOC)
                locs_text = [ent.text.lower() for ent in locs]
                gerar_wordcloud(locs_text, nuvem_filepath("locais"))

                # WordCloud de Organizações (ORG)
                orgs_text = [ent.text.lower() for ent in orgs]
                gerar_wordcloud(orgs_text, nuvem_filepath("organizacoes"))

                messagebox.showinfo(
                    "Sucesso",
                    f"Arquivo CSV principal salvo em:\n{full_path}\n\n"
                    f"Arquivos auxiliares gerados:\n"
                    f"- Sentimento por sentença: {sentimento_csv_path}\n"
                    f"- Lista de Locais: {locais_csv_path}\n\n"
                    f"Nuvens de palavras geradas:\n"
                    f"  {nuvem_filepath('verbos')}\n"
                    f"  {nuvem_filepath('substantivos')}\n"
                    f"  {nuvem_filepath('adjetivos')}\n"
                    f"  {nuvem_filepath('adverbios')}\n"
                    f"  {nuvem_filepath('locais')}\n"
                    f"  {nuvem_filepath('organizacoes')}",
                    parent=janela_pai
                )
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}", parent=janela_pai)
