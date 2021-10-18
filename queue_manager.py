from process_manager import Process

class Queue:
    def __init__(self, n: int):
        self.buffer = []
        self.max_quantum = n
        self.quantum = self.max_quantum

    def insert(self, p: Process):
        self.buffer.append(p)

    def run(self):
        process = self.buffer.pop(0)
        process.run()


queue = [[],[]]

i = 0

def schedule(p : Process):
    global queue

    priority = 0 if p.priority == 0 else 1
    queue[priority].append(p)

def run():
    global i

    p = None
    if len(queue[i]) > 0:
        p = queue[i].pop(0)
        p.run()
    
        if not p.is_finished():
            queue[i].append(p)
    
    if i == 0:
        if len(queue[1]) != 0:
            i = 1
    else:
        if len(queue[0]) != 0:
            i = 0

    return p


