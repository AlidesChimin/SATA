# converter_tabela.py
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import spacy
import csv
import os

# Carrega o modelo spaCy diretamente
nlp = spacy.load('pt_core_news_sm')

def converter_texto_tabela(janela_pai):
    """
    1) Cria a tabela principal (pares Source-Target) a partir de tokens
       que são VERB, ADJ, NOUN.
    2) Cria três tabelas adicionais (nomes, locais, organizacoes) em formato CSV,
       cada uma com pares Source-Target baseados apenas nas entidades PER, LOC, ORG,
       respectivamente.
    """
    arquivo_entrada = filedialog.askopenfilename(
        title="Selecione o arquivo TXT",
        filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
    )
    if not arquivo_entrada:
        return

    try:
        # 1. Lê o texto
        with open(arquivo_entrada, 'r', encoding='utf-8') as f:
            texto = f.read()

        # 2. Processa com spaCy
        doc = nlp(texto)

        # 3. Tabela principal (VERB, ADJ, NOUN)
        tokens_principais = [token.text for token in doc if token.pos_ in ('VERB', 'ADJ', 'NOUN')]
        pairs_principais = [
            (tokens_principais[i], tokens_principais[i+1])
            for i in range(len(tokens_principais) - 1)
        ]

        # 3.1 Pede onde salvar o CSV principal
        arquivo_saida_principal = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")],
            title="Salvar tabela principal como"
        )
        if not arquivo_saida_principal:
            return

        # 3.2 Salva CSV principal
        with open(arquivo_saida_principal, 'w', encoding='utf-8', newline='') as csvfile:
            escritor = csv.writer(csvfile)
            escritor.writerow(['Source', 'Target'])
            escritor.writerows(pairs_principais)

        messagebox.showinfo(
            "Sucesso", 
            f"Tabela principal salva em:\n{arquivo_saida_principal}",
            parent=janela_pai
        )

        # 4. Tabelas adicionais: nomes (PER), locais (LOC), organizações (ORG)
        pessoas = [ent for ent in doc.ents if ent.label_ == 'PER']
        locs = [ent for ent in doc.ents if ent.label_ == 'LOC']
        orgs = [ent for ent in doc.ents if ent.label_ == 'ORG']

        # Converte em listas de strings
        pessoas_text = [ent.text for ent in pessoas]
        locs_text = [ent.text for ent in locs]
        orgs_text = [ent.text for ent in orgs]

        # Gera bigramas para cada categoria
        pares_nomes = [
            (pessoas_text[i], pessoas_text[i+1])
            for i in range(len(pessoas_text) - 1)
        ]
        pares_locais = [
            (locs_text[i], locs_text[i+1])
            for i in range(len(locs_text) - 1)
        ]
        pares_orgs = [
            (orgs_text[i], orgs_text[i+1])
            for i in range(len(orgs_text) - 1)
        ]

        # 5. Usa a mesma base do arquivo principal para nomear novos CSV
        base_filename = os.path.splitext(os.path.basename(arquivo_saida_principal))[0]
        output_dir = os.path.dirname(arquivo_saida_principal)

        # 5.1 Tabela de nomes (PER)
        nomes_csv = os.path.join(output_dir, f"{base_filename}_nomes.csv")
        with open(nomes_csv, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Source', 'Target'])
            writer.writerows(pares_nomes)

        # 5.2 Tabela de locais (LOC)
        loc_csv = os.path.join(output_dir, f"{base_filename}_locais.csv")
        with open(loc_csv, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Source', 'Target'])
            writer.writerows(pares_locais)

        # 5.3 Tabela de organizacoes (ORG)
        org_csv = os.path.join(output_dir, f"{base_filename}_organizacao.csv")
        with open(org_csv, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Source', 'Target'])
            writer.writerows(pares_orgs)

        # Mensagem de sucesso
        messagebox.showinfo(
            "Sucesso", 
            f"Tabelas adicionais geradas:\n"
            f"{nomes_csv}\n"
            f"{loc_csv}\n"
            f"{org_csv}",
            parent=janela_pai
        )

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}", parent=janela_pai)
