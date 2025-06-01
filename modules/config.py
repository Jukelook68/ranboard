class settings:
    def __init__(self):
        #settings
        self.maxclicks = 100
        self.triggerKey = "w"
        self.soundApi = "MME"

#set at runtime
class globals:
    def __init__(self):
        self.path = ""
        self.dir_list = []
        options = {}