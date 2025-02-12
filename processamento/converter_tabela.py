# processamento/converter_tabela.py
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import spacy
import csv

# Reutiliza o modelo spaCy
nlp = spacy.load('pt_core_news_sm')

def converter_texto_tabela(janela_pai):
    arquivo_entrada = filedialog.askopenfilename(
        title="Selecione o arquivo TXT",
        filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
    )
    if arquivo_entrada:
        try:
            with open(arquivo_entrada, 'r', encoding='utf-8') as f:
                texto = f.read()
            doc = nlp(texto)
            tokens_filtrados = [token.text for token in doc if token.pos_ in ('VERB', 'ADJ', 'NOUN')]
            pares = [(tokens_filtrados[i], tokens_filtrados[i+1]) for i in range(len(tokens_filtrados)-1)]
            arquivo_saida = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")],
                title="Salvar arquivo como"
            )
            if arquivo_saida:
                with open(arquivo_saida, 'w', encoding='utf-8', newline='') as csvfile:
                    escritor = csv.writer(csvfile)
                    escritor.writerow(['Source', 'Target'])
                    escritor.writerows(pares)
                messagebox.showinfo("Sucesso", "O arquivo CSV foi criado com sucesso.", parent=janela_pai)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}", parent=janela_pai)

