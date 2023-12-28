import tkinter as tk
from tkinter import messagebox

class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")

        # Lista de tarefas
        self.tasks = []

        # Entrada para adicionar tarefa
        self.task_entry = tk.Entry(root, width=30)
        self.task_entry.pack(pady=10)

        # Botão para adicionar tarefa
        add_button = tk.Button(root, text="Adicionar Tarefa", command=self.add_task)
        add_button.pack(pady=5)

        # Lista para exibir tarefas
        self.task_listbox = tk.Listbox(root, width=50)
        self.task_listbox.pack()

        # Botão para remover tarefa
        remove_button = tk.Button(root, text="Remover Tarefa", command=self.remove_task)
        remove_button.pack(pady=5)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.update_task_list()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Atenção", "Por favor, insira uma tarefa.")

    def remove_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            self.tasks.pop(selected_task_index[0])
            self.update_task_list()

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()