import memory_management as memory

class Process:
    
    pid_count = 0
    
    def __init__(self, offset, time, priority, execution_time, blocks, printer, scanner, modem, driver):
        self.priority = priority
        self.execution_time = execution_time
        self.offset = offset
        self.blocks = blocks
        self.printer = printer
        self.scanner = scanner
        self.modem = modem
        self.driver = driver
        Process.pid_count += 1
        self.pid = Process.pid_count

    def run(self):
        self.execution_time -= 1
        if self.execution_time == 0:
            print("Processo finalizado")


processes_input = open("input/processes.txt")
files_input = open("input/files.txt")

processes = []

for p in processes_input:
    processes.append(p.split(", "))

    #priority = process_info[1]
    #size = process_info[3]
    #if mem.spaceAvailable(priority, size):
    #    offset = mem.allocate(size)
    #    processes.append(Process(offset, *process_info))
    #processes.append(Process(0, *info))

processes_input.close()
files_input.close()