import tkinter as tk
from interface import ControleEstoque
import banco_de_dados

# Criar banco de dados caso não exista
banco_de_dados.criar_tabela()

# Criar a janela principal do programa
root = tk.Tk()
app = ControleEstoque(root)

# Iniciar o loop da interface gráfica
root.mainloop()
