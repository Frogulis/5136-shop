import Store
from UserAccount import UserAccount
from CustomerAccount import CustomerAccount

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

    def viewProduct(self, productId):
        pass    #TODO

    def browseProducts(self):
        return Store.products

    def register(self, name, pwd, phone, address, loggedIn=False):
        uid = Store.Store.generateNewCustomerId()
        UserAccount.setId(uid)
        UserAccount.setName(name)
        UserAccount.setPassword(pwd)
        UserAccount.setLoggedIn(True)
        CustomerAccount.setPhoneNumber(phone)
        CustomerAccount.setAddress(address)
        CustomerAccount.setShoppingCart(None)
        CustomerAccount.setBalance(0.00)
        CustomerAccount.setLoggedIn(True)

