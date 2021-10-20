""" Implementa a abstração de gerenciamento de filas, ou escalonador de processos, do pseudo-SO."""
from process_manager import Process

class QueueManager:
    """ O Gerenciador de filas é a entidade responsável por alocar
        os processos prontos na CPU da forma mais eficiente.
        O algoritmo usado é o de múltiplas filas de prioridade,
        onde a fila mais prioritária é não-preemptiva e as outras são preemptivas.
    """
    def __init__(self):
        self.queues = [[],[],[],[]]     # inicializa as 4 filas, ordenadas por prioridade
        self.count = 0                  # contador de processos, que não pode ultrapassar 1000

    def schedule(self, proc: Process):
        """ Escala um processo para ser executado na CPU, após sua criação.
            Coloca o processo na fila correspondente à sua prioridade.
            Caso a prioridade seja maior que 3, ele entrará na fila 3.
        """
        self.count += 1
        if self.count > 1000:
            print("Limite máximo de processos atingido")
        i = min(proc.priority, 3)
        self.queues[i].append(proc)

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
                # o processo precisa ser reinserido nas filas, a menos que tenha finalizado
                if not proc.is_finished():
                    # se for processo da fila prioritária, volta pra frente da fila (sem preemptar)
                    if i == 0:
                        queue.insert(0, proc)
                    # se for de outra fila, mas não há outros processos nela, reinsere na mesma
                    elif not queue:
                        queue.append(proc)
                    # caso haja processos na fila atual, o processo irá para o fim da fila de baixo
                    else:
                        next_i = min(i+1, len(self.queues)-1)
                        self.queues[next_i].append(proc)
                return proc
        # se percorreu todas as filas e nenhum processo foi encontrado, retorna None
        return None

    def print(self):
        """ Função que imprime a configuração atual das filas de processos,
            representando cada processo com seu PID.
        """
        string = "Filas:\n"
        for queue in self.queues:
            string += '['
            for proc in queue:
                string += str(proc.pid) + ' '
            string += ']\n'
        return string
