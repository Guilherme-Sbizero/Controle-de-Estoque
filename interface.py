import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import banco_de_dados
import pandas as pd

class ControleEstoque:
    def __init__(self, root):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root = root
        self.root.title("Controle de Estoque")
        self.root.geometry("1000x550")
        self.root.configure(bg="#f0f2f5")
        self.ordem_crescente = True

        self.label_titulo = ctk.CTkLabel(root, text="Controle de Estoque", font=ctk.CTkFont(size=18, weight="bold"), text_color="#1f2937")
        self.label_titulo.pack(pady=10)

        self.frame_principal = ctk.CTkFrame(root, fg_color="#f0f2f5", corner_radius=0)
        self.frame_principal.pack(fill="both", expand=True, padx=10, pady=5)

        # Frame formulário
        self.frame_form = ctk.CTkFrame(self.frame_principal, fg_color="#ffffff", corner_radius=10)
        self.frame_form.pack(side="left", fill="y", padx=10, pady=5)

        def criar_label(texto, linha):
            label = ctk.CTkLabel(self.frame_form, text=texto, text_color="#4b5563")
            label.grid(row=linha, column=0, sticky="w", pady=5)

        def criar_entry(linha):
            entry = ctk.CTkEntry(self.frame_form, width=150)
            entry.grid(row=linha, column=1, pady=5)
            return entry

        criar_label("Produto:", 0)
        self.entry_produto = criar_entry(0)

        criar_label("Quantidade:", 1)
        self.entry_quantidade = criar_entry(1)

        criar_label("Preço (R$):", 2)
        self.entry_preco = criar_entry(2)

        criar_label("Tipo:", 3)
        self.combo_tipo = ttk.Combobox(self.frame_form, values=["Unidade", "Caixa"], state="readonly", width=17)
        self.combo_tipo.grid(row=3, column=1, pady=5)
        self.combo_tipo.current(0)

        def criar_botao(texto, comando, cor="#3b82f6"):
            return ctk.CTkButton(self.frame_form, text=texto, command=comando, fg_color=cor, hover_color="#2563eb", text_color="white")

        criar_botao("➕ Adicionar", self.adicionar_item).grid(row=4, column=0, columnspan=2, sticky="we", pady=5)
        criar_botao("✏️ Editar", self.editar_item).grid(row=5, column=0, columnspan=2, sticky="we", pady=5)
        criar_botao("🗑️ Excluir", self.excluir_item, cor="#ef4444").grid(row=6, column=0, columnspan=2, sticky="we", pady=5)
        criar_botao("⬇️ Exportar Excel", self.exportar_para_excel, cor="#10b981").grid(row=7, column=0, columnspan=2, sticky="we", pady=5)

        # Frame Tabela
        self.frame_tabela = ctk.CTkFrame(self.frame_principal, fg_color="#f0f2f5", corner_radius=0)
        self.frame_tabela.pack(side="right", fill="both", expand=True)

        # Barra de pesquisa com placeholder
        self.entry_pesquisa = ctk.CTkEntry(self.frame_tabela, placeholder_text="Pesquisar produto...", width=300)
        self.entry_pesquisa.pack(pady=5)
        self.entry_pesquisa.bind("<KeyRelease>", self.filtrar_tabela)

        self.btn_ordenar = ctk.CTkButton(self.frame_tabela, text="Ordenar por Preço ↑", command=self.ordenar_por_preco, fg_color="#3b82f6", hover_color="#2563eb", text_color="white")
        self.btn_ordenar.pack(pady=5)

        self.frame_tabela_scroll = ctk.CTkFrame(self.frame_tabela)
        self.frame_tabela_scroll.pack(fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#ffffff", foreground="#000000", rowheight=25, fieldbackground="#ffffff")
        style.map("Treeview", background=[("selected", "#cbd5e1")])

        self.tree = ttk.Treeview(self.frame_tabela_scroll, columns=("Produto", "Quantidade", "Preço", "Tipo"), show="headings")
        for col in ("Produto", "Quantidade", "Preço", "Tipo"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.scrollbar = ttk.Scrollbar(self.frame_tabela_scroll, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.selecionar_item)
        self.carregar_dados()

    # Métodos iguais aos anteriores
    def carregar_dados(self, ordenar=False):
        self.tree.delete(*self.tree.get_children())
        conexao = banco_de_dados.conectar()
        cursor = conexao.cursor()
        ordem_sql = "ASC" if self.ordem_crescente else "DESC"
        query = f"SELECT produto, quantidade, preco, tipo FROM estoque ORDER BY preco {ordem_sql}" if ordenar else "SELECT produto, quantidade, preco, tipo FROM estoque"
        cursor.execute(query)
        self.dados_estoque = cursor.fetchall()
        conexao.close()
        for index, item in enumerate(self.dados_estoque):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=item, tags=(tag,))
        self.tree.tag_configure("evenrow", background="#f9fafb")
        self.tree.tag_configure("oddrow", background="#e5e7eb")

    def filtrar_tabela(self, event):
        filtro = self.entry_pesquisa.get().lower()
        self.tree.delete(*self.tree.get_children())
        for index, item in enumerate(self.dados_estoque):
            if filtro in item[0].lower():
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=item, tags=(tag,))

    def ordenar_por_preco(self):
        self.ordem_crescente = not self.ordem_crescente
        self.btn_ordenar.configure(text=f"Ordenar por Preço {'↑' if self.ordem_crescente else '↓'}")
        self.carregar_dados(ordenar=True)

    def adicionar_item(self):
        produto = self.entry_produto.get()
        quantidade = self.entry_quantidade.get()
        preco = self.entry_preco.get()
        tipo = self.combo_tipo.get()
        if produto and quantidade and preco:
            try:
                preco = float(preco)
                quantidade = int(quantidade)
                conexao = banco_de_dados.conectar()
                cursor = conexao.cursor()
                cursor.execute("INSERT INTO estoque (produto, quantidade, preco, tipo) VALUES (?, ?, ?, ?)", (produto, quantidade, preco, tipo))
                conexao.commit()
                conexao.close()
                self.carregar_dados()
                messagebox.showinfo("Sucesso", "Item adicionado com sucesso!")
            except ValueError:
                messagebox.showwarning("Erro", "Quantidade e preço devem ser numéricos!")
        else:
            messagebox.showwarning("Erro", "Preencha todos os campos!")

    def selecionar_item(self, event):
        item = self.tree.focus()
        if item:
            valores = self.tree.item(item, "values")
            self.entry_produto.delete(0, "end")
            self.entry_quantidade.delete(0, "end")
            self.entry_preco.delete(0, "end")
            self.entry_produto.insert(0, valores[0])
            self.entry_quantidade.insert(0, valores[1])
            self.entry_preco.insert(0, valores[2])
            self.combo_tipo.set(valores[3])

    def editar_item(self):
        item = self.tree.focus()
        if item:
            valores_antigos = self.tree.item(item, "values")
            novo_produto = self.entry_produto.get()
            nova_quantidade = self.entry_quantidade.get()
            novo_preco = self.entry_preco.get()
            novo_tipo = self.combo_tipo.get()
            try:
                nova_quantidade = int(nova_quantidade)
                novo_preco = float(novo_preco)
                conexao = banco_de_dados.conectar()
                cursor = conexao.cursor()
                cursor.execute("""UPDATE estoque SET produto=?, quantidade=?, preco=?, tipo=?
                                  WHERE produto=? AND quantidade=? AND preco=? AND tipo=?""",
                               (novo_produto, nova_quantidade, novo_preco, novo_tipo, *valores_antigos))
                conexao.commit()
                conexao.close()
                self.carregar_dados()
                messagebox.showinfo("Sucesso", "Item editado com sucesso!")
            except ValueError:
                messagebox.showwarning("Erro", "Quantidade e preço devem ser numéricos!")

    def excluir_item(self):
        item = self.tree.focus()
        if item:
            valores = self.tree.item(item, "values")
            confirmar = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este item?")
            if confirmar:
                conexao = banco_de_dados.conectar()
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM estoque WHERE produto=? AND quantidade=? AND preco=? AND tipo=?", valores)
                conexao.commit()
                conexao.close()
                self.carregar_dados()

    def exportar_para_excel(self):
        arquivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx")])
        if arquivo:
            dados = [self.tree.item(child)["values"] for child in self.tree.get_children()]
            df = pd.DataFrame(dados, columns=["Produto", "Quantidade", "Preço", "Tipo"])
            df.to_excel(arquivo, index=False)
            messagebox.showinfo("Exportado", f"Dados exportados para: {arquivo}")


if __name__ == "__main__":
    root = ctk.CTk()
    app = ControleEstoque(root)
    root.mainloop()
