import Store

class StoreController:
    def __init__(self):
        self.loginDetail = None  # store the Id of the user that currently logged in
        self.store = Store.Store()

    def addProduct(self):
        pass  # TODO

    # the controller have the customerId stored already, so we do not need the parameter
    def checkOut(self):
        pass  # TODO

    def displayOrderHistory(self):
        pass  # TODO

    def displayStartMenu(self):
        pass  # TODO



    def editProduct(self):
        pass  # TODO

    def login(self):
        # TODO ask for input of userName and password
        self.loginDetail = ""  # should be userId here

    def logout(self):
        # ask for confirm from user
        self.loginDetail = None

    def searchProduct(self):
        pass  # TODO

    def viewProduct(self):


