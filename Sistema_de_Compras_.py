import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

banco = sqlite3.connect("sistema_compras_calin_123.db")
cursor = banco.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS compras (
    id INTEGER PRIMARY KEY AUTOINCREMENT, produto TEXT, categoria TEXT,
    quantidade INTEGER, valor REAL, total REAL)""")
banco.commit()

def salvar():
    produto = entrada_produto.get().strip()
    categoria = combo_categoria.get()
    try:
        quantidade = int(entrada_quantidade.get())
        valor = float(entrada_valor.get().replace(",", "."))
        if not produto or not categoria:
            messagebox.showwarning("Atenção", "Preencha produto e categoria!"); return
        if quantidade <= 0 or valor < 0: raise ValueError
        total = quantidade * valor
        cursor.execute("INSERT INTO compras (produto, categoria, quantidade, valor, total) VALUES (?, ?, ?, ?, ?)",
                       (produto, categoria, quantidade, valor, total))
        banco.commit(); listar(); limpar()
        messagebox.showinfo("Sucesso", "Compra cadastrada!")
    except ValueError:
        messagebox.showerror("Erro", "Informe quantidade e valor válidos!")

def listar():
    for item in tabela.get_children(): tabela.delete(item)
    cursor.execute("SELECT * FROM compras ORDER BY id DESC")
    soma = 0
    for registro in cursor.fetchall():
        tabela.insert("", tk.END, values=(registro[0], registro[1], registro[2],
                      registro[3], f"R$ {registro[4]:.2f}", f"R$ {registro[5]:.2f}"))
        soma += registro[5]
    label_total.config(text=f"TOTAL DAS COMPRAS: R$ {soma:.2f}")

def excluir():
    selecionado = tabela.selection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione uma compra!"); return
    id_compra = tabela.item(selecionado[0])["values"][0]
    if messagebox.askyesno("Confirmar", "Excluir esta compra?"):
        cursor.execute("DELETE FROM compras WHERE id=?", (id_compra,))
        banco.commit(); listar()

def limpar():
    entrada_produto.delete(0, tk.END); combo_categoria.set("")
    entrada_quantidade.delete(0, tk.END); entrada_valor.delete(0, tk.END)

def fechar():
    banco.close(); janela.destroy()

janela = tk.Tk()
janela.title("Sistema de Compras - Lucas")
janela.geometry("900x650"); janela.configure(bg="#EAF0F6")
cabecalho = tk.Frame(janela, bg="#17365D", height=75)
cabecalho.pack(fill="x"); cabecalho.pack_propagate(False)

tk.Label(cabecalho, text="SISTEMA DE COMPRAS", font=("Arial", 22, "bold"),
         bg="#17365D", fg="white").pack(pady=20)
formulario = tk.LabelFrame(janela, text="Cadastro de Produtos", font=("Arial", 12, "bold"),
                           bg="white", fg="#17365D", padx=20, pady=15)
formulario.pack(fill="x", padx=25, pady=20)
tk.Label(formulario, text="Nome do Produto:", bg="white").grid(row=0, column=0, sticky="w")
entrada_produto = tk.Entry(formulario, width=35)
entrada_produto.grid(row=0, column=1, padx=10, pady=8)
tk.Label(formulario, text="Categoria:", bg="white").grid(row=1, column=0, sticky="w")
combo_categoria = ttk.Combobox(formulario, values=["Informática", "Alimentos", "Limpeza",
                                                   "Eletrônicos", "Papelaria", "Outros"],
                               state="readonly", width=32)
combo_categoria.grid(row=1, column=1, padx=10, pady=8)
tk.Label(formulario, text="Quantidade:", bg="white").grid(row=2, column=0, sticky="w")
entrada_quantidade = tk.Entry(formulario, width=35)
entrada_quantidade.grid(row=2, column=1, padx=10, pady=8)
tk.Label(formulario, text="Valor Unitário (R$):", bg="white").grid(row=3, column=0, sticky="w")
entrada_valor = tk.Entry(formulario, width=35)
entrada_valor.grid(row=3, column=1, padx=10, pady=8)

botoes = tk.Frame(janela, bg="#EAF0F6"); botoes.pack(pady=5)
tk.Button(botoes, text="SALVAR COMPRA", command=salvar, bg="#198754", fg="white",
          font=("Arial", 10, "bold"), width=18).grid(row=0, column=0, padx=8)
tk.Button(botoes, text="EXCLUIR", command=excluir, bg="#DC3545", fg="white",
          font=("Arial", 10, "bold"), width=15).grid(row=0, column=1, padx=8)
tk.Button(botoes, text="LIMPAR", command=limpar, bg="#F0AD4E", fg="black",
          font=("Arial", 10, "bold"), width=15).grid(row=0, column=2, padx=8)

frame_tabela = tk.Frame(janela, bg="#EAF0F6")
frame_tabela.pack(fill="both", expand=True, padx=25, pady=15)
colunas = ("ID", "Produto", "Categoria", "Quantidade", "Valor", "Total")
tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=9)
for coluna in colunas:
    tabela.heading(coluna, text=coluna)
    tabela.column(coluna, width=110, anchor="center")
tabela.column("Produto", width=180); tabela.pack(fill="both", expand=True)
label_total = tk.Label(janela, text="TOTAL DAS COMPRAS: R$ 0,00", bg="#17365D",
                       fg="white", font=("Arial", 15, "bold"), pady=12)
label_total.pack(fill="x")
listar(); janela.protocol("WM_DELETE_WINDOW", fechar)
janela.mainloop()
