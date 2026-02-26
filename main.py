import sqlite3, time

def create_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks(
                   id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                   name VARCHAR(40) NOT NULL,
                   status TEXT NOT NULL
                   )''')
    connection.commit() 

connection = sqlite3.connect("database.db")
cursor = connection.cursor()
create_table()

def request_op():
    while True:
        try:
            op = int(input('''[1] = Adicionar tarefas
[2] = Listar tarefas
[3] = Listar tarefas por status
[4] = Editar tarefas
[5] = Remover tarefas
[9] = Finalizar lista
Digite a operação desejada: '''))
            if op in [1, 2, 3, 4, 5, 9]: return op
        except ValueError:pass
        print('Digite uma alternativa válida!')

def request_id():
    if has_tasks():
        while True:
            try:
                id = int(input('Digite o id da tarefa(0 retorna ao menu): '))
                if id == 0 : return None
                cursor.execute('SELECT COUNT(*) FROM tasks WHERE ID = ?', (id,))
                ids = cursor.fetchone()[0]
                if ids > 0: return id   
                else: print('id não encontrado!')
            except ValueError: print('Digite um id válido!')
    print('Nenhuma tarefa encontrada!')
    return None

def has_tasks():
    cursor.execute('SELECT 1 FROM tasks LIMIT 1')
    tasks = cursor.fetchone()
    if tasks: return True
    else: return False

def request_name_task(prompt = 'Digite o nome da tarefa: ', allow_empty = False, default_name = None):
        name = input(prompt).strip()
        if not name and allow_empty: 
            return default_name

        return name if name else None

def request_status_task():
    while True:
        try:
            status = int(input('''[0] = Não iniciada
[1] = Em andamento
[2] = Finalizada
[9] = Voltar ao menu
Digite o status desejado: '''))
        except ValueError: pass
        if status in [0, 1, 2, 9]:
            if status == 0: status = 'Não iniciada'
            elif status == 1: status = 'Em andamento'
            elif status == 2: status = 'Finalizada'
            else: status = None
            return status
        print('Digite uma opção válida!')

def add_task(name):
    cursor.execute('''INSERT INTO tasks(name, status)
                    VALUES(?, ?)''', (name, "Não iniciada"))
    connection.commit()
        

def show_tasks(status = None):
    if has_tasks():

        if status:
            cursor.execute('SELECT * FROM tasks WHERE status = ?', (status, ))
        else: cursor.execute('SELECT * FROM tasks')
            
        tasks = cursor.fetchall()
        return tasks
    else: return None

def print_tasks(tasks):
    print(f"{'ID':<3} | {'Nome da Tarefa':<25} | {'Status'}")
    print("-" * 50)
    for t in tasks:
        print(f"{t[0]:<3} | {t[1]:<25} | {t[2]}")
    

def update_task(id, name, status):
    cursor.execute('''UPDATE tasks
                   SET name = ?, status = ? 
                    WHERE id = ?''', (name, status, id))
    connection.commit()
    
def remove_task(id):
    cursor.execute('DELETE FROM tasks WHERE id = ?', (id, ))
    connection.commit()

    
while True:
    print('-' * 40) 
    op = request_op()
    print('-' * 40)

    if op == 1:
        name = request_name_task()
        if name: add_task(name)
        else: continue

    elif op in [2, 3]:
        if op == 2: tasks = show_tasks()
        else: 
            status = request_status_task()
            if not status: continue
            tasks = show_tasks(status) 
        if tasks: print_tasks(tasks)
        else: print('Nenhuma tarefa encontrada!')

    elif op == 4:
        id = request_id()
        if not id: continue
        cursor.execute('SELECT name FROM tasks WHERE id = ?', (id,))
        current_name = cursor.fetchone()[0]
        name = request_name_task(f"Digite o novo nome [{current_name}]: ", allow_empty=True, default_name=current_name)
        status = request_status_task()
        if not status: continue
        update_task(id, name, status)

    elif op == 5:
        id = request_id()
        if not id: continue
        remove_task(id)

    elif op == 9:    
        print('\033[33mEncerrando o programa...\033[m')
        time.sleep(1.5)
        print('Volte quando precisar!')
        break

connection.close()