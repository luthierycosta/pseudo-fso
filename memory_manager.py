""" Implementa a abstração de memória do pseudo-SO,
    que será usada pela gerência de memória e também pela gerência de arquivos.
"""
from process_manager import Process

class Memory:
    """ Representa uma memória em mapa de bits, onde cada caractere (bit) representa um bloco
        de memória. Um caractere 0 na posição i significa que o bloco i está livre;
        um caractere 1 significa que está ocupado.
    """
    def __init__(self, size: int):
        self.memory = '0'*size
        self.size = size

    def allocate(self, start: int, size: int):
        """ Usa a estratégia first-fit para alocação, isto é,
            procura o primeiro espaço disponível a partir da posição start.
        """
        address = self.memory.find('0'*size, start)
        if address != -1:
            self.memory = self.memory[:address] + '1'*size + self.memory[address+size:]
        return address

    def free(self, start: int, size: int):
        """ Atribui 0 aos blocos no intervalo informado,
            não importando os valores anteriores.
        """
        self.memory = self.memory[:start] + '0'*size + self.memory[start+size:]

class MemoryManager:
    """ Representa o módulo de gerência de memória do SO, que é responsável por alocar processos
        usando várias partições de memória simples, ou seja, objetos da classe Memory,
        sem uso de uma abstração de memória virtual.
    """
    def __init__(self, *partitions: int):
        self.memory = [Memory(n) for n in partitions]

    def allocate(self, proc: Process):
        """ Tenta alocar p usando a estratégia first-fit,
            sempre procurando a partir do bloco 0.
        """
        i = 0 if proc.priority == 0 else 1
        return self.memory[i].allocate(0, proc.blocks)

    def free(self, proc: Process):
        """ Obtém os dados de endereço inicial e tamanho do processo p
            e chama o método free do objeto de memória.
        """
        i = 0 if proc.priority == 0 else 1
        return self.memory[i].free(proc.offset, proc.blocks)
        