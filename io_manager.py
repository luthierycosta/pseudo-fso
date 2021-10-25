"""Implementa o módulo de Entrada e Saída do pseudo-SO."""
from copy import deepcopy
from process_manager import Process
class IO:
    """ Representa todo o módulo de E/S, onde os recursos de E/S
        como impressoras e drivers SATA são mapeados numa mesma estrutura.
    """
    def __init__(self):
        # Cada número associado ao recurso representa sua qtd. disponível.
        self.resources = {
            "printer": 2,
            "scanner": 1,
            "modem": 1,
            "driver": 2
        }
        # Conjunto de processos atualmente com recursos alocados.
        self.processes = set()

    def open(self, proc: Process):
        """ Simula a alocação de recursos ao processo proc.
            A informação de quais recursos devem ser alocados
            estão como atributos no objeto proc.
        """
        # Faz cópia do estado atual dos recursos
        backup = deepcopy(self.resources)
        for resource, value in self.resources.items():
            # Para cada recurso, testa se o respectivo atributo em proc está marcado
            if getattr(proc, resource) != 0:
                # Se o valor atual no dicionário for maior que 0, permite alocação
                if value > 0:
                    self.resources[resource] -= 1
                    self.processes.add(proc.pid)
                # Caso contrário, não permite, imprime erro e restaura estado anterior
                else:
                    print(f"O processo {proc.pid} não conseguiu alocar o recurso: {resource}")
                    self.resources = backup
                    return

    def close(self, proc: Process):
        """ Simula a liberação de recursos do processo proc, ao fim de sua execução."""
        if proc.pid not in self.processes:
            return
        # É necessário ler novamente o objeto proc para saber o que liberar
        for resource, _ in self.resources.items():
            if getattr(proc, resource) != 0:
                self.resources[resource] += 1
                self.processes.discard(proc.pid)

# Teste temporário
io = IO()
io.open(Process("1, 1, 1, 1, 1, 1, 0, 0"))
io.open(Process("1, 1, 1, 1, 1, 1, 0, 0"))
print(io.resources)
