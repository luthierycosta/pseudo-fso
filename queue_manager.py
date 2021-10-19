from process_manager import Process

""" 
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
"""

class QueueManager:
    def __init__(self):
        self.queues = [[],[],[],[]]
        self.count = 0

    def schedule(self, process: Process):
        self.count += 1
        if self.count > 1000:
            print("Limite máximo de processos atingido")
        i = min(process.priority, 3)
        self.queues[i].append(process)

    def run(self):
        for (i, queue) in enumerate(self.queues):
            if queue:
                process = queue.pop(0)
                process.run()
                if not process.is_finished():
                    if i == 0:
                        queue.insert(0, process)
                    elif not queue:
                        queue.append(process)
                    else:
                        next_i = min(i+1, len(self.queues)-1)
                        self.queues[next_i].append(process)
                return process
        return None

    def print(self):
        string = "Filas:\n"
        for queue in self.queues:
            string += '['
            for process in queue:
                string += str(process.pid) + ' '
            string += ']\n'
        return string
