from process_manager import Process

memory = [
    "0" * 64,
    "0" * 1024
]

def allocate(p: Process):
    global memory
    size = p.blocks
    part = 0 if p.priority == 0 else 1
    first_block = memory[part].find("0"*size)
    if first_block != -1:
        memory[part] = memory[part].replace("0"*size, "1"*size, 1)

    return first_block

def free(p: Process):
    global memory
    begin = p.offset
    size = p.blocks
    part = 0 if p.priority == 0 else 1
    memory[part] = memory[part][:begin] + "0"*size + memory[part][begin+size:]
    