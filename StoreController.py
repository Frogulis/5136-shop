from collections import OrderedDict

from Store import Store
from UserAccount import UserAccount
from CustomerAccount import CustomerAccount
from UserInterface import UserInterface

class StoreController:
    def __init__(self):
        self.loginDetail = None  # store the Id of the user that currently logged in
        self.store = Store()


    def addProduct(self):
        inputs = UserInterface.displayForm("Please give the details of the new product",
                                           [('Name', 'nstring'), ('Unit of Measure', 'nstring')
                                               , ('Price per unit', 'money'), ('Source/Origin', 'nstring')
                                               , ('shelfLife', 'int')])
        self.store.addProduct(inputs[0], inputs[1], inputs[2], inputs[3], inputs[4])
        self.store.writeStore()
        UserInterface.writeLine("Product added.")

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

    def displayMenuReturnOption(self):
        while True:
            menuItems = OrderedDict() #stays in input order
            menuItems['B'] = ('Browse Products', 'Enter B to browse the list of products')
            menuItems['S'] = ('Search Products', 'Enter S to search products by keyword')
            if not self.loginDetail: #nobody logged in
                menuItems['R'] = ('Register', 'Enter R to register an account')
                menuItems['L'] = ('Login', 'Enter L to login to your account')
            else:
                menuItems['O'] = ('View Order History', 'Enter O to view order history')
                menuItems['T'] = ('Logout', 'Enter T to logout')
                if self.loginDetail == 'owner':
                    menuItems['A'] = ('Add Product', 'Enter A to add a product')
                    menuItems['C'] = ('Remove Customer', 'Enter C to remove a customer')
                    menuItems['E'] = ('Edit Product', 'Enter E to edit a product')
                    menuItems['RP'] = ('Remove Product', 'Enter RP to remove a product')
                else:
                    menuItems['M'] = ('Manage Account', 'Enter M to manage your account')
                    menuItems['SC'] = ('View Shopping Cart', 'Enter SC to view shopping cart')
            menuItems['X'] = ("Exit", 'Enter X to exit')
            request = UserInterface.displayList("Monash Fruit and Vegetable Store",
                                                list(menuItems.values()),
                                                "Please enter one of the above options to continue").upper().strip()
            if request not in menuItems.keys():
                UserInterface.writeLine("Invalid input, please try again")
            else:
                return request

    def viewAllProductID(self):
        toBeDisplayed = []
        productIds = []
        for product in self.store.getProducts():
            id = product.getId()
            nameUnitSource = product.getName() + " " + product.getUnit() + " " + product.getSource()
            toBeDisplayed.append((id, nameUnitSource))
            productIds.append(id)
        UserInterface.displayList("All product and their IDs: ", toBeDisplayed, "", False)
        return productIds


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
                                          [('Customer ID', 'nstring'), ('Password', 'nstring')])
        try:
            if inputs[0] == 'owner':
                self.store.owner.logIn(inputs[1])
                self.loginDetail = self.store.owner.getId()
            else:
                customer = self.store.getCustomer(inputs[0])
                customer.logIn(inputs[1])
                self.loginDetail = customer.getId()
            UserInterface.writeLine("Successfully logged in!")
        except Exception:
            UserInterface.writeLine("Invalid Customer ID and password combination")

    #ML
    def logout(self):
        # ask for confirm from user
        if self.loginDetail is None:
            pass
        elif self.loginDetail == 'owner':
            self.store.owner.setLoggedIn(False)
        else:
            customer = self.store.getCustomer(self.loginDetail)
            customer.setLoggedIn(False)

        self.loginDetail = None
        UserInterface.writeLine("Logged out successfully.")

    def register(self):
        inputs = UserInterface.displayForm("Please enter your user details to register.\nYour userID will be generated automatically.",
            [('Type your password', 'nstring'), ('Type your password again', 'nstring'),
             ('Enter your name', 'nstring'), ('Enter your phone number', 'nstring'),
             ('Enter your address', 'nstring')])
        while inputs[0] != inputs[1]:
            inputs[0:2] = UserInterface.displayForm("Passwords don't match! Please try again",
                [('Type your password', 'nstring'), ('Type your password again', 'nstring')])
        newCustomer = self.store.addCustomer(inputs[0], inputs[2], inputs[3], inputs[4])
        self.store.writeStore()
        UserInterface.writeLine("Successfully registered! Your ID is {}. You will be automatically logged in.".format(newCustomer.getId()))
        self.loginDetail = newCustomer.getId()

    def searchProduct(self):
        keyword = UserInterface.displayForm("Search Product: Please input the product you would like to search: ", [('name', 'string')])
        # here keyword is a list, so the "real" keyword  is keyword[0]
        matchingList = self.store.searchProductByName(keyword[0])
        toBeDisplayed =[]
        displayNumber = 0
        for matchingProduct in matchingList:
            tuple0 = displayNumber
            theRest = matchingProduct.getName() + matchingProduct.getUnit() + " " + matchingProduct.getSource()
            newTuple = (tuple0, theRest)
            toBeDisplayed.append(newTuple)
            displayNumber += 1
        choice = UserInterface.displayList("The matching products are: ", toBeDisplayed, "Which product to choose? X to go back.")

        validInput = False
        while not validInput:
            if choice == "x" or choice == "X":
                validInput = True
                #The end of this method
            else:
                matchIndex = 0
                stop = False
                while not stop and matchIndex < len(matchingList):
                    if choice == str(matchIndex):
                        stop = True
                    else:
                        matchIndex += 1
                if stop is False:
                    choice = input("Please enter a valid input.")
                else:
                    validInput = True
                    self.viewProductByPrice(matchingList[matchIndex].getId())

    def viewProductByPrice(self, productId):
        product = self.store.getProduct(productId)
        tuples = [('name',product.getName())]
        tuples.append(('source', product.getSource()))
        tuples.append(('unit', product.getUnit()))
        tuples.append(('Original Price', product.getOriginalPrice()))

        UserInterface.displayList("Product details: ", tuples, "", False)
        priceGroup = product.getPriceGroups()
        if priceGroup == {}:
            UserInterface.writeLine("There is no stock of this product.")
        else:
            toBeDisplayed = []
            for everyPrice in priceGroup:
                newtuple0 = "Price: " + str(everyPrice)
                newtuple1 = "Quantity: " + str(priceGroup[everyPrice])
                toBeDisplayed.append((newtuple0,newtuple1))

                UserInterface.displayList("The available stocks are: ", toBeDisplayed, False)

    # not used in our program
    def viewProduct(self, productId):
        products = Store.getProducts()
        # products = [['20001', 'Apple (kg) bag', 'ea'], ['20002', 'Green apple', 'kg']
            #, ['20003', 'Dutch carrots', 'ea'], ['20004', 'Watermelon', 'ea'], ['20005', 'Rock Melon', 'ea']]
        i = 0
        found = False
        while found == False:
            if products[i][0] != productId:
                i += 1
            else:
                found = True
        #print(products[i])
        return products[i]

    def viewShoppingCart(self, customerId):
        shoppingCart = self.store.getCustomer(customerId).getShoppingCart().getProductsInCart()
        listToBeDisplayed = []
        for listhaha in shoppingCart:
            pName = self.store.getProduct(listhaha[0]).getName()
            listToBeDisplayed.append((pName,listhaha[1:]))
        UserInterface.displayList("Products in Shopping Cart", listToBeDisplayed, "", False)
        # return something

    def browseProducts(self):
        # keyword = UserInterface.displayForm("Search Product: Please input the product you would like to search: ", [('name', 'string')])
        # here keyword is a list, so the "real" keyword  is keyword[0]

        matchingList = self.store.getProducts()
        toBeDisplayed =[]
        displayNumber = 0
        for matchingProduct in matchingList:
            tuple0 = displayNumber
            theRest = matchingProduct.getName() + " " + matchingProduct.getUnit() + " " + matchingProduct.getSource()
            newTuple = (tuple0, theRest)
            toBeDisplayed.append(newTuple)
            displayNumber += 1
        choice = UserInterface.displayList("The matching products are: ", toBeDisplayed, "Which product to choose? X to go back.")

        validInput = False
        while not validInput:
            if choice == "x" or choice == "X":
                validInput = True
                #The end of this method
            else:
                matchIndex = 0
                stop = False
                while not stop and matchIndex < len(matchingList):
                    if choice == str(matchIndex):
                        stop = True
                    else:
                        matchIndex += 1
                if stop is False:
                    choice = input("Please enter a valid input.")
                else:
                    validInput = True
                    self.viewProductByPrice(matchingList[matchIndex].getId())



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

    def removeProduct(self):
        idlist = self.viewAllProductID()
        validInput = False
        while not validInput:
            productIdInput = input("Please input id, x to quit")
            # productIdInput = UserInterface.displayForm("Id of the product to be removed: ", "please input Id, X to cancel ")
            if productIdInput in idlist:
                self.store.removeProduct(productIdInput)
                validInput = True
                UserInterface.writeLine("Product removed.")
            elif productIdInput.upper() == "X":
                validInput = True
            else:
                pass

    def editProduct(self):
        idlist = self.viewAllProductID()
        validInput = False
        while not validInput:
            productIdInput = input("Please input id, x to quit")
            # productIdInput = UserInterface.displayForm("Id of the product to be removed: ", "please input Id, X to cancel ")
            if productIdInput in idlist:
                while True:
                    UserInterface.writeLine("You would like to change product: ")
                    metadataToBeEdited = input("A. Name  B. Unit C. Source D. Original Price E. Cancel").upper()
                    if metadataToBeEdited == "A":
                        newName = input("New product name: ")
                        self.store.editProductName(productIdInput,newName)
                        break
                    elif metadataToBeEdited == "B":
                        newUnit = input("New Unit:")
                        self.store.editProductUnit(productIdInput,newUnit)
                        break
                    elif metadataToBeEdited == "C":
                        newSource = input("New Source:")
                        self.store.editProductSource(productIdInput,newSource)
                        break
                    elif metadataToBeEdited == "D":
                        newOP = input("New Original Price")
                        self.store.editProductOriginalPrice(productIdInput,newOP)
                        break
                    elif metadataToBeEdited == "E":
                        break
                    else:
                        UserInterface.writeLine("Invalid Input")
                validInput = True
                UserInterface.writeLine("Product edited.")
            elif productIdInput.upper() == "X":
                validInput = True
            else:
                pass




if __name__ == '__main__':
    s = StoreController()
    while True:
        request = s.displayMenuReturnOption()
        if request == 'A':  # ML
            s.addProduct()
        elif request == 'B':
            s.browseProducts()
        elif request == 'S':
            s.searchProduct()
        elif request == 'E':
            s.editProduct()
        elif request == 'O':
            s.displayOrderHistory(s.loginDetail)
        elif request == 'R':
            s.register()
        elif request == 'L':
            s.login()
        elif request == 'RP':
            s.removeProduct()
        elif request == 'SC':
            #viewshoppingcart
            pass
        elif request == 'T':
            s.logout()
        elif request == 'X':
            s.store.writeStore()
            exit()
        else:
            UserInterface.writeLine("Sorry, that input is not available right now")


    # s.loginDetail = ''
    # s.displayStartMenu()
    # exit()
    # #s.searchProduct('ot')
    # s.store.addCustomer('cs1','cs1','0450563312','add1')
    # s.store.addCustomer('cs2','cs3','0450563312','add1')
    # s.store.addCustomer('cs3','cs3','0450563312','add1')
    # s.store.addProduct('apple','kg',5, 'China', 10)
    # s.store.addProduct('banana', 'kg', 3, 'China', 5)
    # s.store.getProduct('1').addBatch(20)
    # s.store.getProduct('2').addBatch(30)
    #
    # s.editBatchQuantity('1','1')