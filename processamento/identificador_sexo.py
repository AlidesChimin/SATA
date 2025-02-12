# processamento/identificador_sexo.py
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import pandas as pd
import gender_guesser.detector as gender

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

