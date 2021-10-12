from process_manager import Process

class Memory:

    def __init__(self, size: int):
        self.memory = "0" * size

    def allocate(self, size: int):
        first_block = self.memory.find("0"*size)
        if first_block != -1:
            self.memory = self.memory.replace("0"*size, "1"*size, 1)

        return first_block

    def free(self, begin: int, size: int):
        self.memory = self.memory[:begin] + "0"*size + self.memory[begin+size:]

class MemoryManager:

    def __init__(self, *partitions: int):
        self.memory = [Memory(n) for n in partitions]

    def allocate(self, p: Process):
        i = 0 if p.priority == 0 else 1
        return self.memory[i].allocate(p.blocks)

    def free(self, p: Process):
        i = 0 if p.priority == 0 else 1
        return self.memory[i].free(p.offset, p.blocks)
        