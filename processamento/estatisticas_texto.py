# processamento/estatisticas_texto.py
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import spacy
import csv
import gender_guesser.detector as gender

nlp = spacy.load('pt_core_news_sm')

def estatisticas_texto(janela_pai):
    arquivo_entrada = filedialog.askopenfilename(
        title="Selecione o arquivo TXT",
        filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
    )
    if arquivo_entrada:
        try:
            with open(arquivo_entrada, 'r', encoding='utf-8') as f:
                texto = f.read()
            doc = nlp(texto)
            verbs = [token for token in doc if token.pos_ == 'VERB']
            adjs = [token for token in doc if token.pos_ == 'ADJ']
            nouns = [token for token in doc if token.pos_ == 'NOUN']
            advs = [token for token in doc if token.pos_ == 'ADV']
            pessoas = [ent for ent in doc.ents if ent.label_ == 'PER']
            locs = [ent for ent in doc.ents if ent.label_ == 'LOC']
            orgs = [ent for ent in doc.ents if ent.label_ == 'ORG']
            detector = gender.Detector()
            pessoas_sexo = [(p.text, detector.get_gender(str(p.text).split()[0])) for p in pessoas]
            homens = sum(1 for _, s in pessoas_sexo if s in ('male', 'mostly_male'))
            mulheres = sum(1 for _, s in pessoas_sexo if s in ('female', 'mostly_female'))
            sents = list(doc.sents)
            num_sents = len(sents)
            avg_sent_length = sum(len(sent) for sent in sents)/num_sents if num_sents > 0 else 0
            stopwords_count = sum(1 for token in doc if token.is_stop)
            total_tokens = len(doc)
            unique_tokens = len(set(t.lemma_.lower() for t in doc if t.is_alpha))
            ttr = unique_tokens / total_tokens if total_tokens > 0 else 0
            full_path = filedialog.asksaveasfilename(
                title="Selecione a pasta e o nome do arquivo para salvar",
                defaultextension=".csv",
                filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")]
            )
            if full_path:
                with open(full_path, 'w', encoding='utf-8', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Categoria", "Valor"])
                    writer.writerow(["Verbos", len(verbs)])
                    writer.writerow(["Adjetivos", len(adjs)])
                    writer.writerow(["Predicados (NOUN)", len(nouns)])
                    writer.writerow(["Advérbios (ADV)", len(advs)])
                    writer.writerow(["Homens", homens])
                    writer.writerow(["Mulheres", mulheres])
                    writer.writerow(["LOC (Locais)", len(locs)])
                    writer.writerow(["ORG (Organizações)", len(orgs)])
                    writer.writerow(["Número de sentenças", num_sents])
                    writer.writerow(["Comprimento médio das sentenças (tokens)", avg_sent_length])
                    writer.writerow(["Stopwords", stopwords_count])
                    writer.writerow(["Diversidade Lexical (TTR)", ttr])
                messagebox.showinfo("Sucesso", f"Arquivo salvo com sucesso em:\n{full_path}", parent=janela_pai)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}", parent=janela_pai)

