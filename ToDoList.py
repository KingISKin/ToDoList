#Imports
import tkinter as tk
from tkinter import messagebox
from tkinter import Entry as tkEntry
from tkinter.ttk import Frame, Label, Button, Entry, Separator, Style
import sqlite3

#Class
class TodoListApp:
    # Inclusão de Banco de Dados
    def __init__(self, root, db_file="todo_list.db"):
        self.root = root
        self.root.title("To-Do List")
        root.geometry('400x500+100+100')
       

        # Conexão ao banco
        self.conn = sqlite3.connect(db_file)
        self.create_table()

        # Variáveis de login
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Página de login
        self.create_login_page()

    # Criação da tabela de usuários caso não exista
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    # Tela de Login
    def create_login_page(self):

        # Label de entrada de nome de usuário
        tk.Label(self.root, text="Nome de usuário:").pack(pady=10)
        username_entry = tk.Entry(self.root, textvariable=self.username_var)
        username_entry.pack(pady=5)

        # Label de entrada de Senha
        tk.Label(self.root, text="Senha:").pack(pady=10)
        password_entry = tk.Entry(self.root, show="*", textvariable=self.password_var)
        password_entry.pack(pady=5)

        # Botão de login
        login_button = tk.Button(self.root, text="Login", command=self.login)
        login_button.pack(pady=10)

        # Botão para a página de registro
        register_button = tk.Button(self.root, text="Registrar", command=self.create_register_page)
        register_button.pack(pady=10)

         # Associar a tecla Enter a todos os botões na página de login
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.bind('<Return>', lambda event=None, widget=widget: widget.invoke())

    def press_enter_on_button(self, event):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.invoke()
       
    # Validação de login no banco
    def login(self):
        # Verifica as credenciais no banco
        username = self.username_var.get()
        password = self.password_var.get()

        query = "SELECT * FROM users WHERE username=? AND password=?"
        result = self.conn.execute(query, (username, password)).fetchone()

        if result:
            # Se Corretas, abrir app
            self.show_todo_list()
        else:
            messagebox.showerror("Erro de Login", "Credenciais inválidas. Tente novamente.")

    # Mostrar Lista
    def show_todo_list(self):
        # Criação da janela principal do app
        main_window = tk.Toplevel(self.root)
        main_window.title("To-Do List")

        # Lista de tarefas
        self.tasks = []

        # Entrada para adicionar tarefa
        self.task_entry = tk.Entry(main_window, width=30)
        self.task_entry.pack(pady=10)

        # Botão para adicionar tarefa
        add_button = tk.Button(main_window, text="Adicionar Tarefa", command=self.add_task)
        add_button.pack(pady=5)

        # Lista para exibir tarefas
        self.task_listbox = tk.Listbox(main_window, width=50)
        self.task_listbox.pack()

        # Botão para remover tarefa
        remove_button = tk.Button(main_window, text="Remover Tarefa", command=self.remove_task)
        remove_button.pack(pady=5)

    # Adicionar tarefa
    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.update_task_list()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Atenção", "Por favor, insira uma tarefa.")

    # Remover tarefa
    def remove_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            self.tasks.pop(selected_task_index[0])
            self.update_task_list()

    # Atualizar Lista de Tarefas
    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

    # Página de Registro
    def create_register_page(self):
        # Oculta a página de login
        self.root.withdraw()

        # Criação da janela de registro
        register_window = tk.Toplevel(self.root)
        register_window.title("Registrar Usuário")

        # Variáveis de registro
        new_username_var = tk.StringVar()
        new_password_var = tk.StringVar()

        # Rótulos e entradas para registro
        tk.Label(register_window, text="Novo usuário:").pack(pady=10)
        new_username_entry = tk.Entry(register_window, textvariable=new_username_var)
        new_username_entry.pack(pady=5)

        tk.Label(register_window, text="Nova senha:").pack(pady=10)
        new_password_entry = tk.Entry(register_window, show="*", textvariable=new_password_var)
        new_password_entry.pack(pady=5)

        # Botão para registrar novo usuário
        register_button = tk.Button(register_window, text="Registrar", command=lambda: self.register_user(new_username_var.get(), new_password_var.get(), register_window))
        register_button.pack(pady=10)

        # Botão para voltar à página de login
        back_to_login_button = tk.Button(register_window, text="Já possui acesso? Faça seu login!", command=lambda: self.back_to_login(register_window))
        back_to_login_button.pack(pady=10)

        # Associar a tecla Enter a todos os botões na página de registro
        for widget in register_window.winfo_children():
            if isinstance(widget, tk.Button):
                widget.bind('<Return>', lambda event=None, widget=widget: widget.invoke())

    # Registrar Usuário
    def register_user(self, new_username, new_password, register_window):
        # Verifica se o novo usuário já existe
        query = "SELECT * FROM users WHERE username=?"
        result = self.conn.execute(query, (new_username,)).fetchone()

        if result:
            messagebox.showerror("Erro de Registro", "Usuário já existe. Escolha um nome de usuário diferente.")
        else:
            # Registra o novo usuário no banco de dados
            insert_query = "INSERT INTO users (username, password) VALUES (?, ?)"
            self.conn.execute(insert_query, (new_username, new_password))
            self.conn.commit()
            messagebox.showinfo("Registro Concluído", "Usuário registrado com sucesso!")

            # Fecha a janela de registro e mostra a página de login
            register_window.destroy()
            self.root.deiconify()

    # Fim do registro
    def back_to_login(self, register_window):

        # Fecha a janela de registro e mostra a página de login
        register_window.destroy()
        self.root.deiconify()
        
#Final do código
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoListApp(root)
    root.configure(bg='#fff')
    root.mainloop()