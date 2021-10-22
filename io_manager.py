from process_manager import Process

class IO:
    def __init__(self):
        self.resources = {
            "printer": 2,
            "scanner": 1,
            "modem": 1,
            "driver": 2
        }

    def open(self, p: Process):
        backup = self.resources
        for resource, value in self.resources.items():
            if getattr(p, resource) != 0:
                if value > 0:
                    self.resources[resource] -= 1
                else:
                    print(f"O processo {p.pid} não conseguiu alocar o recurso: {resource}")
                    self.resources = backup
                    return

    def close(self, p: Process):
        for resource, _ in self.resources.items():
            if getattr(p, resource) != 0:
                self.resources[resource] += 1

io = IO()

io.open(Process("1, 1, 1, 1, 1, 1, 0, 0"))
io.open(Process("1, 1, 1, 1, 1, 1, 0, 0"))
print(io.resources)
