"""Implementa o módulo de Entrada e Saída do pseudo-SO."""
from copy import deepcopy
from process_manager import Process

resources = {   # Dicionário imutável que guarda a qtd. global de cada recurso
        "printer": 2,
        "scanner": 1,
        "modem": 1,
        "driver": 2
    }

class IOManager:
    """ Representa todo o módulo de E/S, onde os recursos de E/S
        como impressoras e drivers SATA são mapeados numa mesma estrutura.
    """
    def __init__(self):
        # Dicionário mutável que guarda a qtd. disponível de recursos da instância
        self.resources = deepcopy(resources)
        # Conjunto de processos atualmente com recursos alocados.

    def open(self, proc: Process):
        """ Simula a alocação de recursos ao processo proc.
            A informação de quais recursos devem ser alocados são atributos do objeto proc.
            Retorna True se todos os recursos desejados conseguiram ser alocados
            e False caso contrário.
        """
        # Faz cópia do estado atual dos recursos, para caso a alocação falhe
        backup = deepcopy(self.resources)
        for resource, amount in self.resources.items():
            # Para cada recurso, testa se o respectivo atributo em proc está marcado.
            attr = getattr(proc, resource)
            # Se o recurso desejado se encaixa no limite atual do recurso, permite alocação
            if attr <= amount:
                self.resources[resource] -= attr
            # Caso contrário, não permite alocação. Ele irá pra lista de bloqueados do escalonador
            else:
                print(f"O processo {proc.pid} foi bloqueado (não conseguiu obter {resource}).")
                self.resources = backup         # Restaura estado anterior dos recursos
                return False
        return True

    def close(self, proc: Process):
        """ Simula a liberação de recursos do processo proc, ao fim de sua execução."""
        for resource, _ in self.resources.items():
            attr = getattr(proc, resource)
            self.resources[resource] += attr

    def overflow(self, proc: Process):
        """ Retorna True se algum recurso desejado por proc é maior que o limite global do recurso.
            Nesse caso, em nenhum momento será possível alocar os recursos a ele.
        """
        for resource, max_amount in resources.items():
            if getattr(proc, resource) > max_amount:
                print(f"O Processo {proc.pid} não conseguiu ser criado (recursos insuficientes).")
                return True
        return False
