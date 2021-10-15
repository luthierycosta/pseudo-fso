from memory_manager import Memory


memory = ""
files = {}

class FileManager:

    def __init__(self, size: int):
        self.memory = Memory(size)
        self.files = {}

    def insert(self, length: int, pos: int=None , pid: int=None):
        pos = pos or memory.find("0"*length)

        # incompleto


def setDriveSize(size: int):
    global memory
    memory = "0" * size

def insertFile(filename: str, length: int, pos :int=None , pid :int=None):
    global memory, files

    if pos is None: 
        pos = memory.find("0"*length)
    
    if pos != -1:
        memory = memory[:pos] + "1"*length + memory[pos+length:]
        files[filename] = (pos, length, pid)
        print(f"O processo {pid} criou o arquivo {filename}.")
    else:
        print(f"O processo {pid} não pôde criar o arquivo {filename} (sem espaço).")
        
    return pos

def removeFile(_filename: str, _pid: int, _priority: int):
    global memory, files
    
    for i, (pos, length, pid) in files.items():
        if i == _filename:
            if _priority == 0 or _pid == pid:
                memory = memory[:pos] + "0"*length + memory[pos+length:]
                del files[i]
                print(f"O processo {_pid} deletou o arquivo {_filename}.")
                break
            else:
                print(f"O processo {_pid} não tem permissão para deletar o arquivo {_filename}.")
        

def findFile(name: str):
    return files[name]

def getFileName(_pos: int):
    for i, (pos, length, _) in files.items():
        if pos <= _pos < pos+length:
            return i
    
    return "-"

def printMemory():
    print("\n\nMapa de alocação do disco:")
    formattedString = " ".join([getFileName(i) for i in range(len(memory))])
    print(f"{formattedString}\n\n")




        





