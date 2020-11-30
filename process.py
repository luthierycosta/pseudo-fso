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