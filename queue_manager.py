""" Implementa a abstração de gerenciamento de filas, ou escalonador de processos, do pseudo-SO."""
from process_manager import Process
from io_manager import IOManager

io = IOManager()

class QueueManager:
    """ O Gerenciador de filas é a entidade responsável por alocar
        os processos prontos na CPU da forma mais eficiente.
        O algoritmo usado é o de múltiplas filas de prioridade,
        onde a fila mais prioritária é não-preemptiva e as outras são preemptivas.
    """
    def __init__(self):
        self.queues = [[],[],[],[]]     # inicializa as 4 filas, ordenadas por prioridade
        self.blocked = []               # inicializa lista de processos bloqueados

    def len(self):
        """ Retorna o tamanho somado de todas as filas de execução."""
        return sum([len(q) for q in self.queues])

    def schedule(self, proc: Process):
        """ Escala um processo para ser executado na CPU, após sua criação.
            Coloca o processo na fila correspondente à sua prioridade.
            Caso a prioridade seja maior que 3, ele entrará na fila 3.
        """
        # Testa se consegue alocar os recursos do processo. Se sim, insere na fila de execução
        if io.open(proc):
            # Se o limite máximo de processos foi atingido, não insere
            if self.len() >= 1000:
                print("Limite máximo de processos atingido")
            # Caso contrário, insere na fila correspondente à sua prioridade
            else:
                i = min(proc.priority, 3)
                self.queues[i].append(proc)
        # Se o processo pede mais recursos que o disponível globalmente, aborta-o
        elif io.overflow(proc):
            proc.finish()
        # Caso contrário, insere na fila de bloqueio pois os recursos serão alocados futuramente
        else:
            self.blocked.append(proc)

    def run(self):
        """ Executa um dado processo por uma unidade de tempo,
            enquanto realiza o escalonamento apropriado nas filas de processos,
            retornando o processo que foi executado, se houver.
        """
        # percorre todas as filas, onde i é o índice da fila
        for (i, queue) in enumerate(self.queues):
            # executa a primeira fila encontrada que possua processos
            if queue:
                # retira primeiro processo da fila e o executa
                proc = queue.pop(0)
                proc.run()
                # caso o processo tenha finalizado, libera recursos e sinaliza processos bloqueados
                if proc.is_finished():
                    io.close(proc)
                    self.signal()
                # caso contrário, reinsere o processo nas filas
                else:
                    # se for processo da fila prioritária, volta pra frente da fila (sem preemptar)
                    if i == 0:
                        queue.insert(0, proc)
                    # se for de outra fila, mas não há outros processos nela, reinsere na mesma
                    elif not queue:
                        queue.append(proc)
                    # caso haja processos na fila atual, o processo irá para o fim da fila de baixo
                    else:
                        next_i = min(i+1, 3)
                        self.queues[next_i].append(proc)
                return proc
        # se percorreu todas as filas e nenhum processo foi encontrado, retorna None
        return None

    def signal(self):
        """ Passa pelos processos bloqueados tentando reinserir um por um nas filas de execução."""
        current_blocked = list(self.blocked)
        # navega pela lista copiada, pois a lista original será alterada ao longo da execução
        for _ in range(len(current_blocked)):
            # retira elemento da lista original
            proc = self.blocked.pop(0)
            # tenta escaloná-lo; pode ir pra execução ou voltar à lista de bloqueados
            self.schedule(proc)

    def print(self):
        """ Função que imprime a configuração atual das filas de processos,
            representando cada processo pelo seu PID.
        """
        string = "Filas:\n"
        for queue in self.queues:
            string += '['
            for proc in queue:
                string += str(proc.pid) + ' '
            string += ']\n'
        return string
