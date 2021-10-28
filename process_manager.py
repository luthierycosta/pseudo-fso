""" O Módulo process_manager contém a classe Process. """
from time import sleep

class Process:
    """ A classe do processo representa as informações úteis de um processo à sua execução
        (contexto de software)
    """
    # Contador global para atribuir PID aos processos criados
    pid_count = 0

    def __init__(self, process: str):
        """Construtor que tem como argumento uma linha do arquivo de processos"""
        # Remove os \n da string, separa em array e converte cada numero para inteiro
        process = [int(x) for x in process.replace("\n","").split(", ")]
        self.init_time  = process[0]
        self.priority   = process[1]
        self.total_time = process[2]
        self.exec_time  = process[2]
        self.blocks     = process[3]
        self.printer    = process[4]
        self.scanner    = process[5]
        self.modem      = process[6]
        self.driver     = process[7]
        self.offset     = None      # Informação atribuida depois pelo gerenciador de memória
        self.pid        = Process.pid_count
        Process.pid_count += 1

    def start(self, address: int):
        """ Simboliza a inicialização de fato do processo, quando ele é alocado na memória
            e está pronto para ser escalonado na CPU.
        """
        self.offset = address
        self.print()

    def print(self):
        """ Imprime os atributos do processo. """
        print('Processo alocado:')
        print(f'PID:        {self.pid}')
        print(f'offset:     {self.offset}')
        print(f'blocks:     {self.blocks}')
        print(f'priority:   {self.priority}')
        print(f'exec. time: {self.exec_time}')
        print(f'printers:   {self.printer}')
        print(f'scanners:   {self.scanner}')
        print(f'modems:     {self.modem}')
        print(f'drives:     {self.driver}\n')

    def run(self):
        """ Representa a execução (consumo) do processo por 1 unidade de tempo """
        print(f"Processo {self.pid} - instrução {self.total_time - self.exec_time + 1}")
        self.exec_time -= 1
        sleep(1)
        if self.is_finished():
            print(f"Processo {self.pid} - finalizado")

    def is_finished(self):
        """ Retorna se o processo encerrou sua execução. """
        return self.exec_time == 0

    def finish(self):
        """ Encerra o processo no caso de ele não ser escalonado."""
        self.exec_time = 0
