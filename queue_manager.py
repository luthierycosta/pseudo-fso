import process_manager as pm

queue = [[],[]]

i = 0

def schedule(p : pm.Process):
    global queue

    priority = 0 if p.get_priority() == 0 else 1
    queue[priority].append(p)

def run():
    global i

    p = None
    if len(queue[i]) > 0:
        p = queue[i].pop(0)
        p.run()
    
        if not p.isFinished():
            queue[i].append(p)
    
    if i == 0:
        if len(queue[1]) != 0:
            i = 1
    else:
        if len(queue[0]) != 0:
            i = 0

    return p


