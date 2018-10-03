class UserAccount:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.loggedIn = False
        self.password = ""

    def getId(self):
        return self.id

    def setId(self, newId):
        self.id = newId

    def getName(self):
        return self.name

    def setName(self, newName):
        self.name = newName

    def getLoggedIn(self):
        return self.loggedIn

    def setLoggedIn(self, newStatus):
        self.loggedIn = newStatus
    

