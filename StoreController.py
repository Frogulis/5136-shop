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
            outputP = ""
            for insufPro in insufficientP:
                outputP = outputP + insufPro.getName() + " "
            raise Exception("Please reduce the quantity of " + outputP + ".")

        confirmMSG = UserInterface.displayConfirm("You are about to check out. ", "Are you sure?")
        if confirmMSG == 'y' or confirmMSG == 'Y':
            try:
                currentCustomer.subtractBalance(totalPrice)
            except Exception:
                topUpValue = UserInterface.displayForm("Please enter the amount: ", [('Amount', 'money')])
                currentCustomer.topUp(topUpValue)
            for eachProduct in shoppingCart:
                eachProduct.deductStock(eachProduct[1],eachProduct[2])
            shoppingCartCopy = shoppingCart[:]
            newOrder = self.store.addOrder(self.loginDetail, shoppingCartCopy, totalPrice)
            #translate order into list of tuples(name, everthing else)
            orderId = newOrder.getOrderId() # str
            newShoppingCart = newOrder.getShoppingCart()
            listOfTuples = []
            for productInCart in newShoppingCart:
                name = productInCart[0]
                rest = str(productInCart[1]) + " " + str(productInCart[2])
                newTuple = (name, rest)
                listOfTuples.append(newTuple)
            UserInterface.writeLine(orderId)
            UserInterface.displayList("The new order details: ", listOfTuples, "OptionString whatever")
            UserInterface.writeLine("The total price is: " + str(newShoppingCart.getTotalPrice()))
        else:
            pass
            # do nothing

    def checkStock(self, desiredQuantity, productId, actualPrice):
        for product in self.store.products:
            if productId == product.id:
                if desiredQuantity <= product.calculateStock(actualPrice):
                    return True
        return False

    def displayOrderHistory(self, uid):
        if uid == 'owner':
            decision = UserInterface.displayItem("Orders to display",
                [("Customers", "Valid customer numbers are between 1 and {}".format(len(self.store.getCustomers())))],
                "Please enter the number of the customer whose orders you would like to see, or leave blank to see all")
            decision = decision.lower().strip()
            if decision == '':
                orders = self.store.getOrderHistoryAsList()
            else:
                if int(decision) < len(self.store.getCustomers()) and int(decision) > 0:
                    orders = self.store.getCustomerOrders(decision)
                else:
                    UserInterface.writeLine("Invalid customer ID")
                    orders = []
        else:
            orders = self.store.getCustomerOrders(uid)

        displayOrders = [("{}:{} -- {}".format(o.getCustomerId(), o.getOrderId(), str(o.transactionDate)),
            str(o.getShoppingCart()) + str(o.getTotalPrice())) for o in orders]
        UserInterface.displayList("Orders", displayOrders, "Please press enter to return")


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
            if request not in menuItems.keys():
                UserInterface.writeLine("Invalid input, please try again")
            else:
                if request == 'O':
                    self.displayOrderHistory(self.loginDetail)
                elif request == 'X':
                    self.store.writeStore()
                    exit()
                else:
                    UserInterface.writeLine("Sorry, that input is not available right now")



    # def editProduct(self,productId):
    #     # get user input
    #     # editOption = pass
    #     while ...:
    #         if editOption == "Name":
    #             #newName = pass
    #             self.store.editProductName(productId, newName)
    #         elif editOption == "Unit":
    #             #newUnit = pass
    #             self.store.editProductUnit(productId, newUnit)
    #         elif editOption == "Original Price":
    #             newPrice = pass
    #             self.store.editProductOriginalPrice(productId, newPrice)
    #         elif editOption == "Source":
    #             newSource = pass
    #             self.store.editProductSource(productId, newSource)
    #         elif editOption == "Shelf Life":
    #             newShelfLife = pass
    #             self.store.editProductShelfLife(productId, newShelfLife)
    #         # show new product details
    #         # ask for confirmation
    #     # TODO

    def editBatchQuantity(self, productId, batchId):
        currentQuantity = self.store.getProduct(productId).getBatch(batchId).getQuantity()
        UserInterface.writeLine("The current quantity is " + str(currentQuantity))
        results = UserInterface.displayForm("Please enter the new quantity", [('Quantity', 'number')]) #input

        newQuantity = float(results[0])
        confirmMsg = UserInterface.displayConfirm("Your new quantity is " + results[0], "Are you sure?")
        if confirmMsg == 'y' or confirmMsg == 'Y':
            self.store.getProduct(productId).getBatch(batchId).setQuantity(newQuantity)
            UserInterface.writeLine("The new quantity is: " + str(newQuantity))
        else:
            UserInterface.writeLine("The action is abandoned.")

    # can only REDUCE quantity by price, adding will cause trouble
    def reduceProductQuantityByPrice(self, productId, actualPrice):
        UserInterface.writeLine("Current quantity at $" + str(actualPrice) + " is "
            + str(self.store.getProduct(productId).calculateStock(actualPrice)))
        results = UserInterface.displayForm("Please enter the new quantity", [('Quantity', 'number')]) #input
        newQuantity = float(results[0])
        self.store.getProduct(productId).deductStock(actualPrice,newQuantity)
        #display new quantity

    #ML
    def login(self):
        inputs = UserInterface.displayForm("Please enter your login details",
                                          [('Customer ID', 'nstring'), ('Password,' 'nstring')])
        try:
            customer = self.store.getCustomer(inputs[0])
            customer.logIn(inputs[1])
            self.loginDetail = customer.getId()
        except Exception:
            UserInterface.writeLine("Invalid Customer ID and password combination")

    def logout(self):
        # ask for confirm from user
        self.loginDetail = None


    # def searchProduct(self):
    #     ## ask for input
    #     keyword = pass
    #     matching = self.store.searchProductByName(keyword)
    #     ## display matching
    #     pass  # TODO

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
    # def register(self):
    #     # requires a lot of inputs
    #     password = pass
    #     name = pass
    #     phoneNum = pass
    #     address = pass
    #     self.store.addCustomer(password, name, phoneNum, address)

    def removeCustomer(self, customerId):
        # display customer details
        # prompt confirmation
        self.store.removeCustomer(customerId)

    def removeProduct(self, productId):
        self.store.removeProduct(productId)





if __name__ == '__main__':
    s = StoreController()
    s.loginDetail = 'owner'
    s.displayStartMenu()
    exit()
    #s.searchProduct('ot')
    s.store.addCustomer('cs1','cs1','0450563312','add1')
    s.store.addCustomer('cs2','cs3','0450563312','add1')
    s.store.addCustomer('cs3','cs3','0450563312','add1')
    s.store.addProduct('apple','kg',5, 'China', 10)
    s.store.addProduct('banana', 'kg', 3, 'China', 5)
    s.store.getProduct('1').addBatch(20)
    s.store.getProduct('2').addBatch(30)

    s.editBatchQuantity('1','1')