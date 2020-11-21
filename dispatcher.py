class Process:
    
    pid_count = 1
    
    def __init__(self, offset, time, priority, execution_time, blocks, printer, scanner, modem, driver):
        self.pid = Process.pid_count
        self.priority = priority
        self.execution_time = execution_time
        self.offset = offset
        self.blocks = blocks
        self.printer = printer
        self.scanner = scanner
        self.modem = modem
        self.driver = driver
        Process.pid_count += 1

    def run(self):
        self.execution_time -= 1
        if self.execution_time == 0:
            print("Processo finalizado")


processes_input = open("input/processes.txt")
files_input = open("input/files.txt")

processes = []

for process in processes_input:
    info = process.split(", ")

    #riority = process_info[1]
    #size = process_info[3]
    #if mem.spaceAvailable(priority, size):
    #    offset = mem.allocate(size)
    #    processes.append(Process(offset, *process_info))
    processes.append(Process(0, *info))


for process in processes:
    print(process.pid)
    print(process.priority)
    print(process.execution_time)
    print(process.offset)
    print(process.blocks)
    print("fim")

processes_input.close()
files_input.close()