class Process:
    
    pid_count = 0
    
    def __init__(self, time, priority, execution_time, blocks, printer, scanner, modem, driver):
        self.processed = False
        self.priority = priority
        self.time = time
        self.execution_time = execution_time
        self.offset = None
        self.blocks = blocks
        self.printer = printer
        self.scanner = scanner
        self.modem = modem
        self.driver = driver
        self.pid = Process.pid_count
        Process.pid_count += 1

    def get_processed(self):
        return self.processed
    def get_priority(self):
        return self.priority
    def get_time(self):
        return self.time
    def get_execution_time(self):
        return self.execution_time
    def get_offset(self):
        return self.offset
    def get_blocks(self):
        return self.blocks
    def get_printer(self):
        return self.printer
    def get_scanner(self):
        return self.scanner
    def get_modem(self):
        return self.modem
    def get_driver(self):
        return self.driver
    def get_pid(self):
        return self.pid
    
    def set_processed(self, processed):
        self.processed = processed
    def set_priority(self, priority):
        self.priority = priority
    def set_time(self, time):
        self.time = time
    def set_execution_time(self, execution_time):
        self.execution_time = execution_time
    def set_offset(self, offset):
        self.offset = offset
    def set_blocks(self, blocks):
        self.blocks = blocks
    def set_printer(self, printer):
        self.printer = printer
    def set_scanner(self, scanner):
        self.scanner = scanner
    def set_modem(self, modem):
        self.modem = modem
    def set_driver(self, driver):
        self.driver = driver
    def set_pid(self, pid):
        self.pid = pid

    def printProcess(self):
        print('Processo alocado:')
        print(f'PID: {self.pid}')
        print(f'offset: {self.offset}')
        print(f'blocks: {self.blocks}')
        print(f'priority: {self.priority}')
        print(f'time: {self.execution_time}')
        print(f'printers: {self.printer}')
        print(f'scanners: {self.scanner}')
        print(f'modems: {self.modem}')
        print(f'drives: {self.driver}\n')

    def run(self):
        self.execution_time -= 1
        print(f"Processo {self.pid} está executando")
        if self.execution_time == 0:
            print("Processo finalizado")