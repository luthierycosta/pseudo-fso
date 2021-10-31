""" Módulo principal do projeto. É o arquivo a ser executado. """
# Importa função sleep para atrasar execução e a deixar entendível
from time import sleep
# Importa restante dos módulos, com exceção do io_manager
from process_manager import Process
from memory_manager import MemoryManager
from file_manager import FileManager
from queue_manager import QueueManager

# Inicializa memória e escalonador
memory = MemoryManager(64, 960)
qm = QueueManager()

# Abre arquivos de entrada de processos e arquivos
processes_input = open("test/processes.txt")
files_input = open("test/files.txt")

# Lista que armazena todos os processos lidos do arquivo
processes = [Process(line) for line in processes_input]

# Inicializa tempo da simulação
TIME = 0
# Simulação executa até todos os processos estarem finalizados
while not all([p.is_finished() for p in processes]):
    print(f"\n\n\n---------------- Tempo = {TIME} ----------------\n")
    # Loop procura pela lista de processos, buscando processos para escalonar na CPU
    for process in processes:
        # Tenta escalonar processo se seu tempo de inicialização corresponde ao tempo atual
        if process.init_time == TIME:
            address = memory.allocate(process)
            if address != -1:
                process.start(address)
                qm.schedule(process)
            else:
                print(f"O processo {process.pid} não conseguiu ser criado (falta de memória).")
                process.finish()

    # Chama execução do escalonador, retornando o processo que foi executado no tempo atual
    print(qm.print()) # imprime filas de escalonamento para monitoramento das filas
    process = qm.run()

    # Se a execução atual foi a última instrução de um processo, libera sua memória
    if process and process.is_finished():
        memory.free(process)

    sleep(0.5)
    TIME += 1

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

# As linhas restantes representam arquivos criados pelos processos
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
