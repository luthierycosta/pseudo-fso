""" Módulo principal do projeto """

from time import sleep
# Importa 
from process_manager import Process
from memory_manager import MemoryManager
from file_manager import FileManager
from queue_manager import QueueManager
# Abre arquivos de entrada
processes_input = open("test/processes.txt")
files_input = open("test/files.txt")

# Inicializa lista de processos
# (lista diferente da lista de processos escalonados na CPU)
processes = [Process(line) for line in processes_input]

memory = MemoryManager(64, 960)
qm = QueueManager()

current_time = 0
while not all([p.is_finished() for p in processes]):

    print(f"\n\n\n---------------- Tempo = {current_time} ----------------\n")
    for process in processes:
        if process.init_time == current_time:
            address = memory.allocate(process)
            if address != -1:
                process.start(address)
                qm.schedule(process)
            else:
                print(f"O processo {process.pid} não conseguiu ser criado (falta de memória).")
                process.finish()

    # Chama execução do escalonador, retornando o processo que foi executado no segundo atual
    print(qm.print())
    process = qm.run()

    if process and process.is_finished():
        memory.free(process)

    sleep(0.5)
    current_time += 1


print("\n--------------------- Operações com arquivos -----------------------\n\n")

# O primeiro número lido de files_input é o tamanho do disco
drive_size = int(files_input.readline())
# Inicializa disco
fm = FileManager(drive_size)

# O segundo é uma quantidade n de arquivos pré-gravados no sistema
for _ in range(int(files_input.readline())):
    # Cada uma das n linhas seguintes é um arquivo
    filename, first_block, length = files_input.readline().split(", ")
    fm.insert(filename, int(length), int(first_block))

# As linhas restantes são arquivos criados pelos processos
for file in files_input:
    # Manipula string para obter o array de dados
    file = file.replace("\n","").split(", ")
    pid, operation, filename = [int(file[0]), int(file[1]), file[2]]

    # Se o processo não existe, pula operação
    if pid not in [p.pid for p in processes]:
        print(f"\nFalha: processo {pid} não existe\n")
        continue

    # operação de inserir arquivo
    if operation == 0:
        length = int(file[3])
        # tenta criar no 1º espaço, segundo o algoritmo first-fit (logo, busca a partir do bloco 0)
        fm.insert(filename, length, 0, pid)
        
    # operação de remover arquivo
    elif operation == 1:
        # na operação de remover, é preciso obter a prioridade do processo lido
        for p in processes:
            if pid == p.pid:
                priority = p.priority
        fm.remove(filename, pid, priority)

    print(f"\nArquivos alocados:\n{fm.files}\n\n")

print(f"\nMapa de ocupação do disco:\n{fm.print()}\n\n")

# Fecha arquivos de entrada
processes_input.close()
files_input.close()