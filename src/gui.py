# gui.py
import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Imports dos módulos de processamento e janelas auxiliares
from processamento.filtro_texto import filtrar_texto
from processamento.converter_tabela import converter_texto_tabela
from processamento.identificador_sexo import identificador_sexo
from processamento.estatisticas_texto import estatisticas_texto
from informacoes.sobre import show_sobre
from informacoes.funcoes import show_funcoes

import tkinter as tk
from tkinter import font

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None

# Classe para criar tooltips (exibições de explicação quando o mouse passa sobre um widget)
class CreateToolTip:
    """
    Cria um tooltip para um widget.
    Exibe a mensagem após 500 ms de espera quando o mouse entra e a esconde quando sai.
    """
    def __init__(self, widget, text="widget info"):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.id = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(500, self.showtip)

    def unschedule(self):
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def showtip(self, event=None):
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class SATA_GUI:
    def __init__(self, master=None):
        # Se não for passado um master, cria uma janela ttkbootstrap
        self.master = master or ttk.Window(themename="darkly")
        self.master.title("Sistema de Análise de Textos Acadêmico - SATA")
        self.master.geometry("600x700")
        self.create_widgets()

    def load_image(self, relative_path, size):
        """
        Carrega a imagem cujo caminho relativo é dado, redimensionando-a para que caiba no tamanho 'size'.
        Se PIL estiver disponível, utiliza-o; caso contrário, usa tk.PhotoImage.
        """
        base_path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_path, relative_path)
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

    def create_widgets(self):
        # --- FRAME DE INTRODUÇÃO ---
        frame_intro = ttk.Frame(self.master, padding=10)
        frame_intro.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Título centralizado
        titulo = ttk.Label(
            frame_intro,
            text="SATA - Sistema de Análise de Textos Acadêmicos",
            font=("Helvetica", 16, "bold"),
            anchor="center"
        )
        titulo.pack(fill="x", pady=(0, 5))
        
        # Frame para o texto explicativo e a logo lado a lado
        frame_explanation = ttk.Frame(frame_intro)
        frame_explanation.pack(fill="x")
        explicacao = (
            "SATA é uma ferramenta desenvolvida para auxiliar pesquisadores, professores "
            "e estudantes na análise de conteúdo (entrevistas, notícias, etc.). Ele utiliza "
            "técnicas avançadas de processamento de linguagem natural para identificar padrões "
            "linguísticos, analisar a estrutura textual, verificar a coerência argumentativa e destacar "
            "elementos relevantes como citações e referências."
        )
        label_explicacao = ttk.Label(
            frame_explanation,
            text=explicacao,
            wraplength=400,
            justify="left"
        )
        label_explicacao.pack(side="left", fill="both", expand=True)
        
        # Carrega a logo do software
        logo_img = self.load_image("img/logo.png", (130, 130))
        if logo_img:
            label_logo = ttk.Label(frame_explanation, image=logo_img)
            label_logo.image = logo_img
            label_logo.pack(side="right", padx=10)

        # --- FRAME DOS BOTÕES DE FUNÇÃO ---
        frame_botoes = ttk.Frame(self.master, padding=10)
        frame_botoes.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        
        # Carrega imagens para os botões
        self.img_filtro    = self.load_image("img/filtro.png", (94, 94))
        self.img_text_plan = self.load_image("img/text_plan.png", (94, 94))
        self.img_sex       = self.load_image("img/sex.png", (94, 94))
        self.img_estat     = self.load_image("img/estat.png", (94, 94))
        
        # Lista de botões (texto, função, estilo, imagem, tooltip)
        botoes = [
            (
                "Filtrar texto",
                lambda: filtrar_texto(self.master),
                PRIMARY,
                self.img_filtro,
                "Abre um arquivo TXT e filtra o texto deixando apenas verbos, adjetivos e substantivos."
            ),
            (
                "Converter texto em tabela",
                lambda: converter_texto_tabela(self.master),
                SUCCESS,
                self.img_text_plan,
                "Converte o texto filtrado em pares (bigramas) e salva como CSV."
            ),
            (
                "Identificador de Sexo",
                lambda: identificador_sexo(self.master),
                WARNING,
                self.img_sex,
                "Lê um arquivo CSV com nomes e identifica o gênero a partir do primeiro nome."
            ),
            (
                "Estatísticas de texto",
                lambda: estatisticas_texto(self.master),
                INFO,
                self.img_estat,
                "Realiza análise estatística do texto e gera métricas salvando os resultados em CSV."
            )
        ]
        
        # Criação dos botões dinamicamente
        for i, (texto, cmd, bootstyle, image, tip) in enumerate(botoes):
            row = i // 2
            col = i % 2
            botao = ttk.Button(
                frame_botoes,
                text=texto,
                command=cmd,
                bootstyle=bootstyle,
                image=image,
                compound="top"
            )
            botao.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            CreateToolTip(botao, text=tip)
        
        frame_botoes.grid_columnconfigure(0, weight=1)
        frame_botoes.grid_columnconfigure(1, weight=1)

        # --- FRAME DOS BOTÕES INFORMATIVOS ---
        frame_info = ttk.Frame(self.master, padding=10)
        frame_info.grid(row=2, column=0, padx=10, pady=10, sticky="se")

        # Botão "Sobre"
        botao_sobre = ttk.Button(
            frame_info,
            text="Sobre",
            command=lambda: show_sobre(self.master),
            bootstyle=SECONDARY
        )
        botao_sobre.grid(row=0, column=0, padx=5)
        CreateToolTip(botao_sobre, text="Exibe informações sobre o software e a licença GPL.")
        
        # Botão "Funções do software"
        botao_funcoes = ttk.Button(
            frame_info,
            text="Funções do software",
            command=lambda: show_funcoes(self.master),
            bootstyle=SECONDARY
        )
        botao_funcoes.grid(row=0, column=1, padx=5)
        CreateToolTip(botao_funcoes, text="Exibe uma lista detalhada das funcionalidades do software.")
        
        frame_info.grid_columnconfigure(0, weight=1)
        frame_info.grid_columnconfigure(1, weight=1)

    def run(self):
        self.master.mainloop()

# Se quiser executar diretamente este arquivo:
if __name__ == "__main__":
    app = SATA_GUI()
    app.run()
