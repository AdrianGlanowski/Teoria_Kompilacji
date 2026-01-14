from errors import UndeclaredVariableError

class Memory:

    def __init__(self, parent, level): # memory name
        self.parent = parent
        self.level = level

        self.variables = dict()
    def has_key(self, name):  # variable name
        return name in self.variables

    def get(self, name):  # gets from memory current value of variable <name>
        if name in self.variables:
            return self.variables[name]
        
        return self.parent.get(name)  

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.variables[name] = value

    def get_parent(self):
        return self.parent

class MemoryStack:
                                                                             
    def __init__(self): # initialize memory stack with memory <memory>
        self.global_memory = Memory(None, 0)
        self.current_memory = self.global_memory

    def get(self, name): # gets from memory stack current value of variable <name>
        return self.current_memory.get(name)

    def put(self, name, value): # sets variable <name> to value <value>
        self.current_memory.put(name, value)

    def push(self): # pushes memory <memory> onto the stack
        self.current_memory = Memory(self.current_memory, self.current_memory.level+1)

    def pop(self): # pops the top memory from the stack
        self.current_memory = self.current_memory.get_parent()

