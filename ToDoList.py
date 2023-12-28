tasks = []
#funções Básicas, adicionar, remover e visualizar tarefas
def add_task(task):
    tasks.append(task)

def rem_task(task):
    if task in tasks:
        task.remove(task)
    else:
        print('Não encontramos sua tarefa, tente novamente')

def view_tasks():
    print('Lista de Tarefas:')
    for index, task in enumerate(tasks, start=1):
        print(f"{index}. {task}")

#Menu de interação ao usuário
def main():
    while True:
        print("\nEscolha uma Opção:")
        print("1. Adicionar Tarefa")
        print("2. Remover Tarefa")
        print("3. Visualizar Tarefas")
        print("4. Sair")
  
        choice = input("Digite o número da opção desejada: ")

        if choice == "1":
            task = input("Digite a nova tarefa: ")
            add_task(task)
        elif choice == "2":
            task = input("Digite a tarefa a ser removida: ")
            rem_task(task)
        elif choice == "3":
            view_tasks()
        elif choice == "4":
            print("Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")
#Execução Do App
if __name__ == "__main__":
    main()
