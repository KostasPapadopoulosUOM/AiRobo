class MemoryHelper:
    def __init__(self, session):
        self.memory = session.service("ALMemory")

    #Helper method to remove an entry from the memory.
    def RemoveMemoryEntry(self, name):
        if self.memory:
            try:
                self.memory.removeData(name)
            except:
                pass
    #Helper method to read a memory entry.
    def GetMemoryEntry(self, name):
        if self.memory:
            try:
                return self.memory.getData(name)
            except:
                pass

    #Helper method to add a memory entry
    def InsertMemoryEntry(self, name, value):
        if self.memory:
            try:
                self.memory.insertData(name, value)
                print("Saved in memory: " + name + " Value:" + str(value))
            except:
                pass

    #Helper method to clear common keys from memory.
    def ClearMemory(self):
        self.RemoveMemoryEntry("Image1")
        self.RemoveMemoryEntry("Image2")
        self.RemoveMemoryEntry("Image3")
        self.RemoveMemoryEntry("Result")
