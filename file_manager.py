memory = ""
files = []

def setDriveSize(size):
    global memory
    memory = "0" * size

def insertFile(filename, length, pos=None):
    global memory, files
    if pos is None: 
        pos = memory.find("0"*length)
    
    if pos != -1:
        memory = memory[:pos] + "1"*length + memory[pos+length:]
        files.append((filename, pos, length))
        
    return pos

def removeFile(filename):
    global memory, files
    for file in files:
        if filename == file[0]:
            first_block = file[1]
            length = file[2]
            memory = memory[:first_block] + "0"*length + memory[first_block+length:]
            del file
            break

def findFile(name):
    for (filename, first_block, length) in files:
        if filename == name:
            return first_block
    
    return -1

def getFileName(pos):
    for (filename, first_block, length) in files:
        if first_block <= pos < first_block+length:
            return filename

    return ""



        





