class Droplet:
    def __init__(self, name, status, memory):
        self.name = name
        self.status = status
        self.memory = memory

    def get_info(self):
        return "%s - %s - %s\n" % (self.name, self.memory, self.status)