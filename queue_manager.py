from process_manager import Process

class QueueManager:
    def __init__(self):
        self.queues = [[],[],[],[]]
        self.count = 0

    def schedule(self, proc: Process):
        self.count += 1
        if self.count > 1000:
            print("Limite máximo de processos atingido")
        i = min(proc.priority, 3)
        self.queues[i].append(proc)

    def run(self):
        for (i, queue) in enumerate(self.queues):
            if queue:
                proc = queue.pop(0)
                proc.run()
                if not proc.is_finished():
                    if i == 0:
                        queue.insert(0, proc)
                    elif not queue:
                        queue.append(proc)
                    else:
                        next_i = min(i+1, len(self.queues)-1)
                        self.queues[next_i].append(proc)
                return proc
        return None

    def print(self):
        string = "Filas:\n"
        for queue in self.queues:
            string += '['
            for proc in queue:
                string += str(proc.pid) + ' '
            string += ']\n'
        return string
