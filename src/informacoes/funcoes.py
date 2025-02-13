# informacoes/funcoes.py
import os
import ttkbootstrap as ttk
import tkinter as tk
from tkinter import font

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None

def load_image(relative_path, size):
    """
    Carrega a imagem cujo caminho relativo é dado, redimensionando-a para que caiba no tamanho 'size'.
    Como este arquivo está em "informacoes", subimos um nível para encontrar a pasta "img" na raiz.
    """
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    image_path = os.path.join(base_dir, relative_path)
    try:
        if Image and ImageTk:
            img = Image.open(image_path)
            img.thumbnail(size)
            return ImageTk.PhotoImage(img)
        else:
            return tk.PhotoImage(file=image_path)
    except Exception as e:
        print(f"Erro ao carregar a imagem {image_path}: {e}")
        return None

def show_funcoes(master):
    funcoes_window = ttk.Toplevel(master)
    funcoes_window.title("Funções e Detalhes do SATA")
    funcoes_window.geometry("900x700")
    
    # Criando um canvas para permitir rolagem se o conteúdo for extenso
    canvas = tk.Canvas(funcoes_window, borderwidth=0, background=funcoes_window.cget("background"))
    frame = ttk.Frame(canvas, padding=10)
    vsb = ttk.Scrollbar(funcoes_window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    
    vsb.grid(row=0, column=1, sticky="ns")
    canvas.grid(row=0, column=0, sticky="nsew")
    funcoes_window.grid_rowconfigure(0, weight=1)
    funcoes_window.grid_columnconfigure(0, weight=1)
    canvas.create_window((4,4), window=frame, anchor="nw")
    
    def onFrameConfigure(canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))
    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
    
    # Título
    title_label = ttk.Label(frame, text="Funções e Detalhes do SATA", font=("Helvetica", 18, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=(0,10))
    
    # Função 1: Filtrar Texto
    img_filtro = load_image("img/filtro.png", (150, 150))
    text_filtro = (
        "Filtrar Texto:\n"
        "• Abre um arquivo TXT contendo o texto a ser analisado.\n"
        "• Utiliza spaCy para processar o texto e filtrar verbos, adjetivos e substantivos.\n"
        "• Gera um novo arquivo com o texto filtrado, facilitando análises mais focadas."
    )
    row = 1
    if img_filtro:
        label_img_filtro = ttk.Label(frame, image=img_filtro)
        label_img_filtro.image = img_filtro  # Mantém referência
        label_img_filtro.grid(row=row, column=0, padx=10, pady=10, sticky="nw")
    label_text_filtro = ttk.Label(frame, text=text_filtro, wraplength=600, justify="left")
    label_text_filtro.grid(row=row, column=1, padx=10, pady=10, sticky="nw")
    
    # Função 2: Converter Texto em Tabela (para ARS)
    img_text_plan = load_image("img/text_plan.png", (150, 150))
    row += 1
    text_text_plan = (
        "Converter Texto em Tabela:\n"
        "• Organiza os tokens filtrados em pares (bigramas) que representam a sequência das palavras.\n"
        "• Exporta o resultado para um arquivo CSV no formato ideal para análise de redes sociais (ARS),\n"
        "  compatível com ferramentas como o Gephi.\n"
        "• Nesta versão, o conversor também cria Tabelas Separadas:\n"
        "    - nomes (PER)\n"
        "    - locais (LOC)\n"
        "    - organizações (ORG)\n"
        "  Cada uma salva em um CSV adicional (ex.: arquivo_nomes.csv), com pares (Source, Target)\n"
        "  exclusivamente para essas entidades."
    )
    if img_text_plan:
        label_img_text_plan = ttk.Label(frame, image=img_text_plan)
        label_img_text_plan.image = img_text_plan
        label_img_text_plan.grid(row=row, column=0, padx=10, pady=10, sticky="nw")
    label_text_text_plan = ttk.Label(frame, text=text_text_plan, wraplength=600, justify="left")
    label_text_text_plan.grid(row=row, column=1, padx=10, pady=10, sticky="nw")
    
    # Função 3: Identificador de Sexo
    img_sex = load_image("img/sex.png", (150, 150))
    row += 1
    text_sex = (
        "Identificador de Sexo:\n"
        "• Lê um arquivo CSV contendo uma coluna 'Nome'.\n"
        "• Utiliza a biblioteca gender_guesser para inferir o gênero com base no primeiro nome.\n"
        "• Adiciona a informação de gênero ao CSV para análises comparativas e estatísticas."
    )
    if img_sex:
        label_img_sex = ttk.Label(frame, image=img_sex)
        label_img_sex.image = img_sex
        label_img_sex.grid(row=row, column=0, padx=10, pady=10, sticky="nw")
    label_text_sex = ttk.Label(frame, text=text_sex, wraplength=600, justify="left")
    label_text_sex.grid(row=row, column=1, padx=10, pady=10, sticky="nw")
    
    # Função 4: Estatísticas de Texto
    img_estat = load_image("img/estat.png", (150, 150))
    row += 1
    text_estat = (
        "Estatísticas de Texto:\n"
        "• Realiza uma análise completa do texto, calculando métricas como:\n"
        "   - Contagem de verbos, adjetivos, substantivos e advérbios;\n"
        "   - Identificação de entidades nomeadas (pessoas, locais, organizações) e stopwords;\n"
        "   - Número total de sentenças e média de tokens por sentença;\n"
        "   - Índice de diversidade lexical (TTR);\n"
        "   - (Novo) Análise de Sentimento (TextBlob) e Geração de Nuvens de Palavras.\n\n"
        "• Exporta os resultados para um arquivo CSV, e ainda:\n"
        "   - (Opcional) Gera arquivos CSV adicionais (ex.: estatistica_sentimento.csv) listando\n"
        "     o sentimento de cada frase;\n"
        "   - Cria diversas nuvens de palavras (verbos, substantivos, adjetivos, advérbios, LOC, ORG)\n"
        "     em arquivos .png, nomeados conforme o CSV principal (ex.: estatistica_nuvem_verbos.png)."
    )
    if img_estat:
        label_img_estat = ttk.Label(frame, image=img_estat)
        label_img_estat.image = img_estat
        label_img_estat.grid(row=row, column=0, padx=10, pady=10, sticky="nw")
    label_text_estat = ttk.Label(frame, text=text_estat, wraplength=600, justify="left")
    label_text_estat.grid(row=row, column=1, padx=10, pady=10, sticky="nw")
    
    # Informações gerais sobre o software
    row += 1
    info_text = (
        "\nDesenvolvedor: Dr. Alides Baptista Chimin Junior\n"
        "Site: http://www.territoriolivre.net\n"
        "Github: https://github.com/AlidesChimin/SATA\n\n"        
    )
    label_info = ttk.Label(frame, text=info_text, wraplength=600, justify="left")
    label_info.grid(row=row, column=0, columnspan=2, padx=10, pady=10, sticky="w")
