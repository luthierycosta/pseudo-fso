from memory_manager import Memory

class FileManager:

    def __init__(self, size: int):
        self.memory = Memory(size)
        self.files = {}

    def insert(self, filename: str, length: int, pos: int=0 , pid: int=None):
        address = self.memory.allocate(pos, length)
        if address != -1:
            self.files[filename] = (address, length, pid)
            block_list = list(range(address, address+length))
            print(f"O processo {pid} criou o arquivo {filename} - blocos {block_list}.")
        else:
            print(f"O processo {pid} não pode criar o arquivo {filename} (falta de espaço).")
        return address

    def remove(self, filename: str, pid: int, priority: int):
        try:
            address, length, _pid = self.files[filename]
            if priority == 0 or _pid == pid:
                self.memory.free(address, length)
                del self.files[filename]
                print(f"O processo {pid} deletou o arquivo {filename}.")
            else:
                print(f"O processo {pid} não tem permissão para deletar o arquivo {filename}.")         
        except KeyError:
            print(f"O processo {pid} não pode deletar o arquivo {filename} porque ele não existe.")

    def find_file(self, filename: str):
        return self.files[filename]
    
    def get_file_at(self, _pos: int):
        for i, (pos, length, _) in self.files.items():
            if pos <= _pos < pos+length:
                return i
        return '-'
    
    def print(self):
        return " ".join([self.get_file_at(i) for i in range(self.memory.size)])
        
