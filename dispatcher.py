import process_manager as pm
import memory_manager as memory
import file_manager as fm
import queue_manager as qm

# Abre arquivos de entrada
processes_input = open("input/processes.txt")
files_input = open("input/files.txt")


# Inicializa lista de processos
# (lista diferente da lista de execução de processos na CPU) 
processes = []
for p in processes_input:
    
    process_info = p.replace("\n","").split(", ")
    process_info = [int(x) for x in process_info]
    process = pm.Process(*process_info)

    processes.append(process)


current_time = 0

while not all([p.isFinished() for p in processes]):

    print(f"\n\n------ Tempo = {current_time} ------\n")
    for process in processes:
        if process.get_time() == current_time:
            offset = memory.allocate(process.get_priority(), process.get_blocks())
            if offset != -1:
                process.set_offset(offset)
                process.printProcess()
                qm.schedule(process)
            else:
                print(f"O processo {process.get_pid()} não conseguiu ser criado (falta de memória).")
                process.set_finished(True)

    # Chama execução do escalonador, retornando o processo que foi executado no segundo atual
    process = qm.run()

    if process is not None and process.isFinished():
        memory.free(process.get_priority(), process.get_offset(), process.get_blocks())

    print("\n")
    current_time += 1


print("\n---------------- Operações com arquivos ------------------\n\n")

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

    # Se o processo não existe, pula operação
    if pid not in [p.get_pid() for p in processes]:
        print(f"\nFalha: processo {pid} não existe\n")
        continue

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
    print(f"\nArquivos alocados:\n{fm.files}\n\n")

fm.printMemory()

# Fecha arquivos de entrada
processes_input.close()
files_input.close()