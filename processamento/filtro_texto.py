# processamento/filtro_texto.py
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import spacy

# Carrega o modelo do spaCy apenas uma vez
nlp = spacy.load('pt_core_news_sm')

def filtrar_texto(janela_pai):
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
            texto_filtrado = ' '.join(tokens_filtrados)
            arquivo_saida = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")],
                title="Salvar arquivo como"
            )
            if arquivo_saida:
                with open(arquivo_saida, 'w', encoding='utf-8') as f:
                    f.write(texto_filtrado)
                messagebox.showinfo("Sucesso", "O arquivo foi processado e salvo com sucesso.", parent=janela_pai)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}", parent=janela_pai)

