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
        if process.isFinished():
            self.quantum = self.max_quantum
        else:
            self.buffer.insert(0, process)
            self.quantum -= 1
        return process

class QueueManager:
    def __init__(self, n: int):
        self.queues = [Queue(n) for _ in range(4)]

    def schedule(self,p: Process):
        self.queues[p.priority].insert(p)

    def run(self):
        for queue in self.queues:
            if queue.buffer:
                return queue.run()
        return None

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


