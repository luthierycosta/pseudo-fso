import process_manager as pm
import memory_manager as memory
import file_manager as fm
import queue_manager as qm

# Abre arquivos de entrada
processes_input = open("input/processes.txt")
files_input = open("input/files.txt")

print("Escolha a quantidade de tempo para rodar a simulação: ")
max_time = int(input())

# Inicializa lista de processos
# (lista diferente da lista de execução de processos na CPU) 
processes = []
for p in processes_input:
    
    process_info = p.replace("\n","").split(", ")
    process_info = [int(x) for x in process_info]
    process = pm.Process(*process_info)

    processes.append(process)


current_time = 0
while current_time <= max_time:
    print(f"Tempo = {current_time}\n")
    for process in processes:
        if process.get_time() == current_time:
            offset = memory.allocate(process.get_priority(), process.get_blocks())
            if offset != -1:
                process.set_offset(offset)
                process.printProcess()
                qm.schedule(process)
            else:
                print(f"O processo {process.get_pid()} não conseguiu ser criado (falta de memória).")

    qm.run()

    print("\n\n")
    current_time += 1




# O primeiro número lido de files_input é o tamanho do disco
drive_size = int(files_input.readline())
fm.setDriveSize(drive_size)

# O segundo é a quantidade n de arquivos a serem pré-alocados
for i in range(int(files_input.readline())):
    # Cada uma das n linhas seguintes é um arquivo
    filename, first_block, length = files_input.readline().split(", ")
    fm.insertFile(filename, int(length), int(first_block))

for file in files_input:
    file = file.replace("\n","").split(", ")
    pid, operation, filename = [int(file[0]), int(file[1]), file[2]]

    priority = None
    for p in processes:
        if pid == p.get_pid():
            priority = p.get_priority()

    if operation == 0:
        length = int(file[3])
        fm.insertFile(filename, length, None, pid)
    elif operation == 1:
        fm.removeFile(filename, pid, priority)

    #print(fm.memory)
    print("\n\nArquivos alocados:\n",fm.files)

fm.printMemory()

# Fecha arquivos de entrada
processes_input.close()
files_input.close()