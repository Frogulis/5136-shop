from collections import OrderedDict

from Store import Store
from UserAccount import UserAccount
from CustomerAccount import CustomerAccount
from UserInterface import UserInterface

class StoreController:
    def __init__(self):
        self.loginDetail = None  # store the Id of the user that currently logged in
        self.store = Store()


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
                pass
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
        while True:
            menuItems = OrderedDict() #stays in input order
            menuItems['B'] = ('Browse Products', 'Enter B to browse the list of products')
            menuItems['S'] = ('Search Products', 'Enter S to search products by keyword')
            if not self.loginDetail: #nobody logged in
                menuItems['R'] = ('Register', 'Enter R to register an account')
                menuItems['L'] = ('Login', 'Enter L to login to your account')
            else:
                menuItems['O'] = ('View Order History', 'Enter O to view order history')
                menuItems['M'] = ('Manage Account', 'Enter M to manage your account')
                if self.loginDetail == 'owner':
                    menuItems['A'] = ('Add Product', 'Enter A to add a product')
                    menuItems['C'] = ('Remove Customer', 'Enter C to remove a customer')
            menuItems['X'] = ("Exit", 'Enter X to exit')
            request = UserInterface.displayList("Monash Fruit and Vegetable Store",
                                                list(menuItems.values()),
                                                "Please enter one of the above options to continue").upper().strip()
            if request in menuItems.values():
                UserInterface.writeLine("You said " + request)
            else:
                UserInterface.writeLine("Invalid option: " + request)



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
        results = UserInterface.displayForm("Please enter the new quantity", [('Quantity', 'number')]) #input
        newQuantity = float(results[0])
        #validate input
        self.store.getProduct(productId).getBatch(batchId).setQuantity(newQuantity)
        #display new quantity

    # can only REDUCE quantity by price, adding will cause trouble
    def reduceProductQuantityByPrice(self, productId, actualPrice):
        UserInterface.writeLine("Current quantity at $" + str(actualPrice) + " is "
            + str(self.store.getProduct(productId).calculateStock(actualPrice)))
        results = UserInterface.displayForm("Please enter the new quantity", [('Quantity', 'number')]) #input
        newQuantity = float(results[0])
        self.store.getProduct(productId).deductStock(actualPrice,newQuantity)
        #display new quantity


    def login(self):
        # TODO ask for input of userName and password
        self.loginDetail = ""  # should be userId here

    def logout(self):
        # ask for confirm from user
        self.loginDetail = None


    def searchProduct(self):
        ## ask for input
        keyword = pass
        matching = self.store.searchProductByName(keyword)
        ## display matching
        pass  # TODO

    #ML
    def viewProduct(self, productId):
        # products = Store.getProducts()
        products = [['20001', 'Apple (kg) bag', 'ea'], ['20002', 'Green apple', 'kg']
            , ['20003', 'Dutch carrots', 'ea'], ['20004', 'Watermelon', 'ea'], ['20005', 'Rock Melon', 'ea']]
        i = 0
        found = False
        while found == False:
            if products[i][0] != productId:
                i += 1
            else:
                found = True
        #print(products[i])
        return products[i]

    def browseProducts(self):
        return self.Store.products

    # def addCustomer(self, password, name, phoneNum, address):
    def register(self):
        # requires a lot of inputs
        password = pass
        name = pass
        phoneNum = pass
        address = pass
        self.store.addCustomer(password, name, phoneNum, address)

    def removeCustomer(self, customerId):
        # display customer details
        # prompt confirmation
        self.store.removeCustomer(customerId)

    def removeProduct(self, productId):
        self.store.removeProduct(productId)





if __name__ == '__main__':
    s = StoreController()
    #s.searchProduct('ot')
    s.viewProduct('20003')
    print(s)