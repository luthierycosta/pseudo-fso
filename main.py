""" Módulo principal do projeto """

from time import sleep
# Importa 
import process_manager as pm
from memory_manager import MemoryManager
#from file_manager import FileManager
import file_manager as fm
import queue_manager as qm

# Abre arquivos de entrada
processes_input = open("test/processes.txt")
files_input = open("test/files.txt")

# Inicializa lista de processos
# (lista diferente da lista de processos escalonados na CPU)
processes = [pm.Process(line) for line in processes_input]

memory = MemoryManager(64, 1024)

current_time = 0
while not all([p.is_finished() for p in processes]):

    print(f"\n\n\n----------- Tempo = {current_time} -----------\n")
    for process in processes:
        if process.init_time == current_time:
            address = memory.allocate(process)
            if address != -1:
                process.offset = address
                process.print()
                qm.schedule(process)
            else:
                print(f"O processo {process.pid} não conseguiu ser criado (falta de memória).")
                process.finish()

    # Chama execução do escalonador, retornando o processo que foi executado no segundo atual
    process = qm.run()

    if process is not None and process.is_finished():
        memory.free(process)

    sleep(1)
    current_time += 1


print("\n---------------- Operações com arquivos ------------------\n\n")

# O primeiro número lido de files_input é o tamanho do disco

drive_size = int(files_input.readline())
# fm = FileManager(size)
fm.setDriveSize(drive_size)

# O segundo é a quantidade n de arquivos a serem pré-alocados
for _ in range(int(files_input.readline())):
    # Cada uma das n linhas seguintes é um arquivo
    filename, first_block, length = files_input.readline().split(", ")
    fm.insertFile(filename, int(length), int(first_block))

for file in files_input:
    file = file.replace("\n","").split(", ")
    pid, operation, filename = [int(file[0]), int(file[1]), file[2]]

    # Se o processo não existe, pula operação
    if pid not in [p.pid for p in processes]:
        print(f"\nFalha: processo {pid} não existe\n")
        continue

    priority = None
    for p in processes:
        if pid == p.pid:
            priority = p.priority

    if operation == 0:
        length = int(file[3])
        fm.insertFile(filename, length, None, pid)
    elif operation == 1:
        fm.removeFile(filename, pid, priority)

    #print(fm.memory)
    print(f"\nArquivos alocados:\n{fm.files}\n\n")

fm.printMemory()

# Fecha arquivos de entrada
processes_input.close()
files_input.close()