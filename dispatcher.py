import process
import memory_manager as memory
import file_manager as fm

# Abre arquivos de entrada
processes_input = open("input/processes.txt")
files_input = open("input/files.txt")

# O primeiro número lido de files_input é o tamanho do disco
drive_size = int(files_input.readline())
fm.setDriveSize(drive_size)

# O segundo é a quantidade n de arquivos a serem pré-alocados
for i in range(files_input.readline()):
    # Cada uma das n linhas seguintes é um arquivo
    filename, first_block, length = files_input.readline().split(", ")
    fm.insertFile(filename, length, first_block)

# Inicializa lista de processos
# (lista diferente da lista de execução de processos na CPU) 
processes = []

for p in processes_input:
    processes.append(p.split(", "))

    #priority = process_info[1]
    #size = process_info[3]
    #if mem.spaceAvailable(priority, size):
    #    offset = mem.allocate(size)
    #    processes.append(Process(offset, *process_info))
    #processes.append(Process(0, *info))

fm.insertFile()

# Fecha arquivos de entrada
processes_input.close()
files_input.close()