from Store import Store
from UserAccount import UserAccount
from CustomerAccount import CustomerAccount

class StoreController:
    def __init__(self):
        self.loginDetail = None  # store the Id of the user that currently logged in
        self.store = Store.Store()

    def addProduct(self, name, unit, originalPrice, source, shelfLife):
        self.store.addProduct(name, unit, originalPrice, source, shelfLife)

    # the controller have the customerId stored already, so we do not need the parameter
    def checkOut(self):
        currentCustomer = self.store.getCustomer(self.loginDetail)
        shoppingCart = currentCustomer.getShoppingCart()
        totalPrice = shoppingCart.getTotalPrice()

        insufficientP = []
        for eachProduct in shoppingCart:
            if not self.checkStock(eachProduct[2], eachProduct[0], eachProduct[1]):
                insufficientP.append(eachProduct)
        if len(insufficientP) > 0: # insufficient stock, return to shopping cart or whatever
            pass # TODO
        else:
            # needs confirmation
            try:
                currentCustomer.subtractBalance(totalPrice)
            except Exception:
                # topUp
            for eachProduct in shoppingCart:
                eachProduct.deductStock(eachProduct[1],eachProduct[2])
            # generate order
            self.store.addOrder(self.loginDetail, shoppingCart, totalPrice)
            # needs display the new order

    def checkStock(self, desiredQuantity, productId, actualPrice):
        for product in self.store.products:
            if productId == product.id:
                if desiredQuantity <= product.calculateStock(actualPrice):
                    return True
        return False

    def displayOrderHistory(self):
        pass  # TODO

    def displayStartMenu(self):
        # ask for user input
        # return
        pass  # TODO

    def editProduct(self,productId):
        # get user input
        editOption = pass
        while ...:
            if editOption == "Name":
                newName = pass
                self.store.editProductName(productId, newName)
            elif editOption == "Unit":
                newUnit = pass
                self.store.editProductUnit(productId, newUnit)
            elif editOption == "Original Price":
                newPrice = pass
                self.store.editProductOriginalPrice(productId, newPrice)
            elif editOption == "Source":
                newSource = pass
                self.store.editProductSource(productId, newSource)
            elif editOption == "Shelf Life":
                newShelfLife = pass
                self.store.editProductShelfLife(productId, newShelfLife)
            # show new product details
            # ask for confirmation
        # TODO

    def editBatchQuantity(self, productId, batchId):
        # TODO
        #display old quantity
        newQuantity = pass #input
        #validate input
        self.store.getProduct(productId).getBatch(batchId).setQuantity(newQuantity)
        #display new quantity

    # can only REDUCE quantity by price, adding will cause trouble
    def reduceProductQuantityByPrice(self, productId, actualPrice):
        # TODO
        # display old quantity
        # ask for new quantity input
        newQuantity = pass
        self.store.getProduct(productId).deductStock(actualPrice,newQuantity)
        #display new quantity


    def login(self):
        # TODO ask for input of userName and password
        self.loginDetail = ""  # should be userId here

    def logout(self):
        # ask for confirm from user
        self.loginDetail = None

    def searchProduct(self):
        pass  # TODO

    def viewProduct(self):
        pass    #TODO

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

