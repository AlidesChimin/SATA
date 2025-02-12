# -*- coding: utf-8 -*-
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter as tk  # Utilizado para o widget Text com barra de rolagem
import spacy
import csv
import pandas as pd
import gender_guesser.detector as gender

# Carrega o modelo de língua portuguesa do spaCy apenas uma vez
nlp = spacy.load('pt_core_news_sm')

# Função para filtrar o texto (mantém a lógica original)
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

# Função para converter texto em tabela
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

# Função para identificar o sexo a partir de um arquivo CSV
def identificador_sexo(janela_pai):
    arquivo_entrada = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv")],
        title="Selecione o arquivo CSV"
    )
    if arquivo_entrada:
        try:
            df = pd.read_csv(arquivo_entrada)
            if 'Nome' not in df.columns:
                messagebox.showerror("Erro", "O arquivo CSV deve conter uma coluna chamada 'Nome'", parent=janela_pai)
                return
            detector = gender.Detector()
            df['Sexo'] = df['Nome'].apply(lambda x: detector.get_gender(str(x).split()[0]))
            arquivo_saida = filedialog.asksaveasfilename(
                title="Selecione a pasta e o nome do arquivo para salvar",
                defaultextension=".csv",
                filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")]
            )
            if arquivo_saida:
                df.to_csv(arquivo_saida, index=False)
                messagebox.showinfo("Sucesso", f"Arquivo salvo com sucesso em:\n{arquivo_saida}", parent=janela_pai)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao processar o arquivo: {e}", parent=janela_pai)

# Função para gerar estatísticas do texto
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

# Função para exibir a janela "Sobre" com informações do desenvolvedor
def show_sobre(master):
    sobre_window = ttk.Toplevel(master)
    sobre_window.title("Sobre")
    sobre_window.geometry("700x100")
    
    # Cria um frame para o widget de texto e a barra de rolagem
    text_frame = ttk.Frame(sobre_window)
    text_frame.pack(fill='both', expand=True)
    
    scrollbar = ttk.Scrollbar(text_frame)
    scrollbar.pack(side='right', fill='y')
    
    # Widget Text com configuração para exibição somente leitura
    text_widget = tk.Text(text_frame, wrap='word', yscrollcommand=scrollbar.set,
                          borderwidth=0, background=sobre_window.cget("background"))
    text_widget.pack(side='left', fill='both', expand=True)
    scrollbar.config(command=text_widget.yview)
    
    sobre_text = (
        """Desenvolvedor: Dr. Alides Baptista Chimin Junior, 2025.
GEPES - Grupo de Pesquisa Redes de Poder, Migrações e Dinâmicas Territoriais - Unicentro
Departamento de Geografia de Irati.
Programa de Pós-Graduação em Geografia.
http://www.territoriolivre.net
Software livre registrado como licença GNU"""
    )
    text_widget.insert("1.0", sobre_text)
    text_widget.config(state="disabled")

# Função para exibir a janela "Funções do softwares" detalhando cada funcionalidade
def show_funcoes(master):
    funcoes_window = ttk.Toplevel(master)
    funcoes_window.title("Funções do softwares")
    funcoes_window.geometry("700x200")
    
    text_frame = ttk.Frame(funcoes_window)
    text_frame.pack(fill='both', expand=True)
    
    scrollbar = ttk.Scrollbar(text_frame)
    scrollbar.pack(side='right', fill='y')
    
    text_widget = tk.Text(text_frame, wrap='word', yscrollcommand=scrollbar.set,
                          borderwidth=0, background=funcoes_window.cget("background"))
    text_widget.pack(side='left', fill='both', expand=True)
    scrollbar.config(command=text_widget.yview)
    
    funcoes_text = (
        "Funções do Software:\n\n"
        "1. Filtrar texto:\n"
        "   Abre um arquivo de texto e utiliza o modelo de linguagem natural (spaCy) para filtrar tokens que são verbos, adjetivos ou substantivos. "
        "Gera um novo arquivo com o texto processado.\n\n"
        "2. Converter texto em tabela:\n"
        "   Processa o texto e converte a sequência de tokens filtrados em pares (Source, Target), salvando o resultado em um arquivo CSV.\n\n"
        "3. Identificador de Sexo:\n"
        "   Lê um arquivo CSV contendo uma coluna 'Nome' e utiliza a biblioteca gender_guesser para identificar o gênero, adicionando essa informação ao CSV.\n\n"
        "4. Estatísticas de texto:\n"
        "   Realiza uma análise estatística do texto, computando contagens de categorias gramaticais, entidades nomeadas e outras métricas, salvando os resultados em um arquivo CSV."
    )
    text_widget.insert("1.0", funcoes_text)
    text_widget.config(state="disabled")

# Função principal que monta a interface
def main():
    # Criação da janela principal com o tema "darkly"
    janela_principal = ttk.Window(themename="darkly")
    janela_principal.title("Sistema de análise de textos acadêmico - SATA")
    janela_principal.geometry("600x300")
    
    # Frame para os botões funcionais
    frame_botoes = ttk.Frame(janela_principal, padding=10)
    frame_botoes.pack(pady=10, fill='x')
    
    botao_filtrar = ttk.Button(frame_botoes, text="Filtrar texto", 
                               command=lambda: filtrar_texto(janela_principal), bootstyle=PRIMARY)
    botao_filtrar.pack(pady=5, fill='x')
    
    botao_converter = ttk.Button(frame_botoes, text="Converter texto em tabela", 
                                 command=lambda: converter_texto_tabela(janela_principal), bootstyle=SUCCESS)
    botao_converter.pack(pady=5, fill='x')
    
    botao_identificar = ttk.Button(frame_botoes, text="Identificador de Sexo",
                                   command=lambda: identificador_sexo(janela_principal), bootstyle=WARNING)
    botao_identificar.pack(pady=5, fill='x')
    
    botao_estatisticas = ttk.Button(frame_botoes, text="Estatísticas de texto",
                                    command=lambda: estatisticas_texto(janela_principal), bootstyle=INFO)
    botao_estatisticas.pack(pady=5, fill='x')
    
    # Frame para os botões informativos "Sobre" e "Funções do softwares"
    frame_info = ttk.Frame(janela_principal, padding=10)
    frame_info.pack(side='bottom', fill='x')
    
    botao_sobre = ttk.Button(frame_info, text="Sobre", 
                             command=lambda: show_sobre(janela_principal), bootstyle=SECONDARY)
    botao_sobre.pack(side='left', padx=5)
    
    botao_funcoes = ttk.Button(frame_info, text="Funções do softwares", 
                               command=lambda: show_funcoes(janela_principal), bootstyle=SECONDARY)
    botao_funcoes.pack(side='left', padx=5)
    
    janela_principal.mainloop()

if __name__ == "__main__":
    main()
