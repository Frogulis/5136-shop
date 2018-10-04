class UserAccount:
    def __init__(self, userId, name, password, loggedIn=False):
        self.userId = userId
        self.name = name
        self.password = password
        self.loggedIn = loggedIn

    def getId(self):
        return self.userId

    def setId(self, newId):
        self.userId = newId

    def getName(self):
        return self.name

    def setName(self, newName):
        self.name = newName

    def getPassword(self):
        return self.password

    def setPassword(self, newPassword):
        self.password = newPassword

    def getLoggedIn(self):
        return self.loggedIn

    def setLoggedIn(self, newStatus):
        self.loggedIn = newStatus

    def logIn(self, uPwd):
        if self.getPassword() == uPwd:
            self.setLoggedIn(True)
        else:
            self.setLoggedIn(False)
            raise Exception("Invalid password")

    

