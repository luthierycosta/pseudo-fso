from process_manager import Process

class Memory:

    def __init__(self, size: int):
        self.memory = '0'*size
        self.size = size

    def allocate(self, start: int, size: int):
        address = self.memory.find('0'*size, start)
        if address != -1:
            self.memory = self.memory[:address] + '1'*size + self.memory[address+size:]

        return address

    def free(self, start: int, size: int):
        self.memory = self.memory[:start] + '0'*size + self.memory[start+size:]

class MemoryManager:

    def __init__(self, *partitions: int):
        self.memory = [Memory(n) for n in partitions]

    def allocate(self, p: Process):
        i = 0 if p.priority == 0 else 1
        return self.memory[i].allocate(0, p.blocks)

    def free(self, p: Process):
        i = 0 if p.priority == 0 else 1
        return self.memory[i].free(p.offset, p.blocks)
        