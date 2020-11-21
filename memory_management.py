memory = [
    "0" * 64,
    "0" * 960
]

def allocate(priority, size):
    part = 0 if priority == 0 else 1
    first_block = memory[part].find("0"*size)
    if first_block != -1:
        memory[part] = memory[part].replace("0"*size, "1"*size, 1)

    return first_block

def free(priority, begin, size):
    part = 0 if priority == 0 else 1
    memory[part] = memory[part][:begin] + "0"*size + memory[part][begin+size:]