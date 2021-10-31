""" Implementa o módulo de gerenciamento de arquivos do pseudo-SO."""
from memory_manager import Memory

class FileManager:
    """ O gerenciador de arquivos comporta inserção e remoção de arquivos
        por parte dos processos do sistema. O método de alocação é a contígua usando
        a estratégia first-fit.
    """

    def __init__(self, size: int):
        # O módulo reaproveita a abstração de memória do módulo gerenciador de memória.
        self.memory = Memory(size)
        # Estrutura para manter os atributos dos arquivos alocados.
        self.files = {}

    def insert(self, filename: str, length: int, pos: int=0 , pid: int=None):
        """ Função de inserir arquivo na memória.
            Pega como parâmetros nome do arquivo, tamanho, posição para alocação e pid do processo.
            Quando pos é diferente de 0 e o pid é nulo, representa um arquivo
            pré-carregado no sistema (inserido por nenhum processo).
        """
        address = self.memory.allocate(pos, length)
        if address != -1:
            self.files[filename] = (address, length, pid)
            block_list = list(range(address, address+length))
            print(f"O processo {pid} criou o arquivo {filename} - blocos {block_list}.")
        else:
            print(f"O processo {pid} não pode criar o arquivo {filename} (falta de espaço).")
        return address

    def remove(self, filename: str, pid: int, priority: int):
        """ Função de remover arquivo da memória.
            Usa os parâmetros pid e prioridade do processo para determinar se tal processo
            tem permissão para remover o arquivo especificado.
        """
        try:
            address, length, _pid = self.files[filename]
            if priority == 0 or _pid == pid:
                self.memory.free(address, length)
                del self.files[filename]
                print(f"O processo {pid} deletou o arquivo {filename}.")
            else:
                print(f"O processo {pid} não tem permissão para deletar o arquivo {filename}.")
        except KeyError:
            print(f"O processo {pid} não pode deletar o arquivo {filename} porque ele não existe.")

    def print(self):
        """ Imprime estado da memória de arquivos. """
        return " ".join([self.get_file_at(i) for i in range(self.memory.size)])

    def get_file_at(self, _pos: int):
        """ Método auxiliar do método print().
            Retorna nome do arquivo presente na posição _pos da memória de arquivos, quando houver.
        """
        for i, (pos, length, _) in self.files.items():
            if pos <= _pos < pos+length:
                return i
        return '-'
