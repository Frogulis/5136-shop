from collections import OrderedDict

from Store import Store
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
        self.store.addProduct(inputs[0], inputs[1], float(inputs[2]), inputs[3], int(inputs[4]))
        self.store.writeStore()
        UserInterface.writeLine("Product added.")

    def checkOut(self):
        currentCustomer = self.store.getCustomer(self.loginDetail)
        shoppingCart = currentCustomer.getShoppingCart()
        totalPrice = shoppingCart.getTotalPrice()
        formattedSC = []
        formattedSC.append(('Index','product name, real price, quantity'))
        for line in shoppingCart.getProductsInCart():
            pname = self.store.getProduct(line[0]).getName()
            newLine = pname + "," + str(line[1]) + "," + str(line[2])
            formattedSC.append((line[0], newLine))
        UserInterface.displayList("Current Shopping Cart", formattedSC, '', False)

        insufficientP = []
        for eachProduct in shoppingCart.getProductsInCart():
            if not self.checkStock(eachProduct[2], eachProduct[0], eachProduct[1]):
                insufficientP.append(eachProduct)
        if len(insufficientP) > 0:  # insufficient stock, return to shopping cart or whatever
            return insufficientP

        confirmMSG = UserInterface.displayConfirm("You are about to check out. ", "Are you sure?")
        if confirmMSG == 'y' or confirmMSG == 'Y':
            if self.store.getCustomer(self.loginDetail).getBalance() < totalPrice:
                UserInterface.writeLine('You do not have sufficient balance. Please go to manage account and top up.')
                return None
            currentCustomer.subtractBalance(totalPrice)

            for eachProduct in shoppingCart.getProductsInCart():
                self.store.getProduct(eachProduct[0]).deductStock(eachProduct[1], eachProduct[2])

            shoppingCartCopy = shoppingCart.getProductsInCart()[:]
            newOrder = self.store.addOrder(self.loginDetail, shoppingCartCopy, totalPrice)
            #translate order into list of tuples(name, everthing else)

            orderId = newOrder.getOrderId() # str
            newShoppingCart = newOrder.getShoppingCart()
            listOfTuples = []
            for productInCart in newShoppingCart.getProductsInCart():
                name = productInCart[0]
                rest = str(productInCart[1]) + " " + str(productInCart[2])
                newTuple = (name, rest)
                listOfTuples.append(newTuple)
            UserInterface.writeLine(orderId)

            UserInterface.displayList("The new order details: ", listOfTuples, "", False)
            UserInterface.writeLine("The total price is: " + str(newShoppingCart.getTotalPrice()))
            currentCustomer.getShoppingCart().setProductsInCart([])
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
        decision = ''
        if uid == 'owner':
            itemised = [(c.getId(), "Name: {}".format(c.getName())) for c in self.store.getCustomers()]
            decision = UserInterface.displayList("Customers",
                itemised,
                "Please enter the number of the customer whose orders you would like to see, or leave blank to see all")
            decision = decision.lower().strip()
            if decision == '':
                orders = self.store.getOrderHistoryAsList()
            else:
                if decision in [i[0] for i in itemised]:
                    orders = self.store.getCustomerOrders(decision)
                else:
                    UserInterface.writeLine("Invalid customer ID")
                    return
        else:
            decision = uid
            orders = self.store.getCustomerOrders(uid)

        if len(orders) > 0:
            displayOrders = [("{}:{} -- {}".format(o.getCustomerId(), o.getOrderId(), str(o.transactionDate)),
                str(o.getShoppingCart()) + str(o.getTotalPrice())) for o in orders]
            UserInterface.displayList("Orders", displayOrders, "", False)
        else:
            UserInterface.writeLine("No orders to display for customer {}".format(decision))

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
                    menuItems['EX'] = ('View Expiring Products', 'Enter EX to view expiring products')
                    menuItems['A'] = ('Add Product', 'Enter A to add a product')
                    menuItems['RC'] = ('Remove Customer', 'Enter RC to remove a customer')
                    menuItems['RP'] = ('Remove Product', 'Enter RP to remove a product')
                else:
                    menuItems['M'] = ('Manage Account', 'Enter M to manage your account')
                    menuItems['UR'] = ('Unregister Account', 'Enter UR to unregister your account')
                    menuItems['SC'] = ('View Shopping Cart', 'Enter SC to view shopping cart')
            menuItems['X'] = ("Exit", 'Enter X to exit')
            request = UserInterface.displayList("Monash Fruit and Vegetable Store",
                                                list(menuItems.values()),
                                                "Please enter one of the above options to continue").upper().strip()
            if request not in menuItems.keys():
                UserInterface.writeLine("Invalid input, please try again")
            else:
                return request

    # default add batch, shelfdate is today
    def restockProduct(self,productId):
        quantity = UserInterface.displayForm("Input how much you wanna restock: ", \
                                               [("restock quantity","number")])
        self.store.getProduct(productId).addBatch(float(quantity[0]))

    def editBatch(self,productId, batchId):
        valid = False
        while not valid:
            choice = UserInterface.displayList("Edit options",[],"A. Edit Batch Price  B. Edit Batch Quantity  Q. Quit")
            if choice.upper() == 'A':
                self.editBatchPrice(productId,batchId)
                valid = True
            elif choice.upper() == 'B':
                self.editBatchQuantity(productId,batchId)
                valid = True
            elif choice.upper() == 'Q':
                valid = True
            else:
                UserInterface.writeLine("Invalid input.")

    def editBatchPrice(self, productId, batchId):
        currentPrice = self.store.getProduct(productId).getBatch(batchId).getActualPrice()
        UserInterface.writeLine("The current quantity is " + str(currentPrice))
        results = UserInterface.displayForm("Please enter the new price", [('Price', 'money')]) #input
        newPrice = float(results[0])
        confirmMsg = UserInterface.displayConfirm("Your new price is " + results[0], "Are you sure?")
        if confirmMsg == 'y' or confirmMsg == 'Y':
            self.store.getProduct(productId).getBatch(batchId).setActualPrice(newPrice)
            UserInterface.writeLine("The new price is: " + str(newPrice))
        else:
            UserInterface.writeLine("The action is abandoned.")

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

    def manageAccount(self):
        customer = self.store.getCustomer(self.loginDetail)

        # option_String = 'Edit Options: 1- Name   2- Password   3- Phone Number   4- Address   5- Balance'
        # keyboardInput = UserInterface.displayList('Account Info.', [('Name', name), ('Password', pwd), ('Phone', phoneNumber)
        #                        , ('Address', address), ('Balance', balance)], option_String)

        while True:
            option_String = 'Edit Options: N- Name   P- Password   C- Phone Number   A- Address   B- Top Up Balance  X- Exit'
            keyboardInput = UserInterface.displayList('Account Info.',
                                                      [('Name', customer.getName()),
                                                      ('Password', customer.getPassword()),
                                                      ('Phone', customer.getPhoneNumber()),
                                                      ('Address', customer.getAddress()),
                                                      ('Balance', customer.getBalance())], option_String).strip().upper()
            if keyboardInput == 'N':
                name = UserInterface.displayForm('Please give a new value for -', [('Name', 'nstring')])
                name = name[0]
                customer.setName(name)
                UserInterface.writeLine('Name updated.')
            elif keyboardInput == 'P':
                pwd = UserInterface.displayForm('Please give a new value for -', [('Password', 'nstring')])
                pwd = pwd[0]
                customer.setPassword(pwd)
                UserInterface.writeLine('Password updated.')
            elif keyboardInput == 'C':
                phoneNumber = UserInterface.displayForm('Please give a new value for -', [('Phone Number', 'nstring')])
                phoneNumber = phoneNumber[0]
                customer.setPhoneNumber(phoneNumber)
                UserInterface.writeLine('Phone number updated.')
            elif keyboardInput == 'A':
                address = UserInterface.displayForm('Please give a new value for -', [('Address', 'nstring')])
                address = address[0]
                customer.setAddress(address)
                UserInterface.writeLine('Address updated.')
            elif keyboardInput == 'B':
                updated = False
                while not updated:
                    balance = UserInterface.displayForm('Please give a new value for -', [('Balance', 'money')])[0]
                    if float(balance) >= 0:
                        customer.topUp(balance)
                        UserInterface.writeLine('Balance updated.')
                        updated = True
                    else:
                        print('Please enter a value greater or equal than zero.')
            elif keyboardInput == 'X':
                self.store.writeStore()
                break

    # can only REDUCE quantity by price, adding will cause trouble
    def reduceProductQuantityByPrice(self, productId, actualPrice):
        totalQ = self.store.getProduct(productId).calculateStock(actualPrice)
        UserInterface.writeLine("Current quantity at $" + str(actualPrice) + " is "\
            + str(totalQ))
        valid = False
        while not valid:
            results = UserInterface.displayForm("Deduct the quantity BY this amount: ", [('Quantity', 'number')])
            newQuantity = float(results[0])
            if newQuantity <= totalQ:
                valid = True
                self.store.getProduct(productId).deductStock(actualPrice,newQuantity)
            else:
                UserInterface.writeLine("The quantity is too much.")
        UserInterface.writeLine("The new quantity is: " + str(self.store.getProduct(productId).calculateStock(actualPrice)))

    # ML
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

    # ML
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
            theRest = matchingProduct.getName() + " " + matchingProduct.getUnit() + " " + matchingProduct.getSource()
            newTuple = (tuple0, theRest)
            toBeDisplayed.append(newTuple)
            displayNumber += 1
        choice = UserInterface.displayList("The matching products are: ", toBeDisplayed, "Which product to choose? X to go back.")

        validInput = False
        while not validInput:
            if choice == "x" or choice == "X":
                validInput = True
                return None
                # The end of this method
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
                    return matchingList[matchIndex].getId()

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
            UserInterface.displayList("The available stocks are: ", toBeDisplayed, "", False)
        # menu of this product
        if self.loginDetail is None:
            pass
        elif self.loginDetail == 'owner':
            # allow owner to edit product
            valid = False
            while not valid:
                UserInterface.writeLine("Next Action: A. View by Batch  B. Edit Product  C. Discount this product Q. Quit")
                ganma = UserInterface.displayList("", [],"")
                if ganma.upper().strip() == "A":
                    self.viewProductByBatch(productId)
                    valid = True
                elif ganma.upper().strip() == "B":
                    self.editProduct(productId)
                    valid = True
                elif ganma.upper().strip() == "C":
                    self.store.getProduct(productId).updateDiscount()
                    valid = True
                elif ganma.upper().strip() == "Q":
                    valid = True
                else:
                    UserInterface.writeLine("Invalid input, try again")
        elif len(priceGroup) > 0:
            self.addToCart(productId, priceGroup)
            # allow customer to addShoppingCart

    def viewProductByBatch(self, productId):
        product = self.store.getProduct(productId)
        batches = product.getBatches()
        tuples = [("BatchId","Price, Quantity, Expiry Date")]
        batchIds = []
        for batch in batches:
            batchId = batch.getBatchID()
            batchIds.append(batchId)
            theRest = str(batch.getActualPrice()) + " " + str(batch.getQuantity()) + " " + str(batch.getExpiryDate())
            tuples.append((batchId,theRest))
        UserInterface.displayList("Batch details: ", tuples, "", False)
        confirm = UserInterface.displayConfirm("Edit batch ","Do you wish to edit Batch?")
        if confirm.lower() == 'y' and len(batchIds) > 0:
            while True:
                batchId = UserInterface.displayForm("Batch Id", [("Please input the batchID you would like to edit.","number")])[0]
                #print(batchIds)
                if batchId in batchIds:
                    self.editBatch(productId,batchId)
                    break
                else:
                    UserInterface.writeLine("Batch Id incorrect. Try again.")
        else:       # ML added else condition so user doesn't get stuck when no batch exists.
            UserInterface.writeLine("No batches to edit.")

    def addToCart(self, productId, priceGroup):
        toAdd = UserInterface.displayConfirm("", "Do you wish to add this Product into shopping cart?")
        if toAdd in ['y', 'Y']:
            # check input, add to cart

            acPrice, pQuantity = None, None
            UserInterface.writeLine("input the price you want. enter 9999 to quit.")
            acPrice = UserInterface.displayForm("select price:", [('', 'money')])[0]
            acPrice = float(acPrice)
            while acPrice not in priceGroup and acPrice != 9999:
                acPrice = UserInterface.displayForm("price not found. select price:", [('', 'money')])[0]
                acPrice = float(acPrice)
            if acPrice != 9999:
                pQuantity = UserInterface.displayForm("input quantity:", [('', 'number')])[0]
                pQuantity = float(pQuantity)
                while pQuantity > priceGroup[acPrice] and pQuantity != 9999:
                    UserInterface.writeLine("quantity larger than stock. input new or 9999 to quit")
                    pQuantity = UserInterface.displayForm("input new:", [('', 'number')])[0]
                    pQuantity = float(pQuantity)
            if acPrice != 9999 and pQuantity != 9999:
                UserInterface.writeLine("selected price: " + str(acPrice) + " Quantity: " + str(pQuantity))
                confirmed = UserInterface.displayConfirm("","confirm to add to shopping cart.")
                if confirmed == 'y':
                    sc = self.store.getCustomer(self.loginDetail).getShoppingCart()
                    sc.addToShoppingCart(productId, acPrice, pQuantity)
                else:
                    pass

    def viewShoppingCart(self):
        shoppingCart = self.store.getCustomer(self.loginDetail).getShoppingCart().getProductsInCart()
        listToBeDisplayed = []
        for listhaha in shoppingCart:
            pName = self.store.getProduct(listhaha[0]).getName()
            theRest = [pName]
            theRest.extend(listhaha[1:])
            listToBeDisplayed.append((listhaha[0],theRest))
        UserInterface.displayList("Products in Shopping Cart", listToBeDisplayed, "", False)
        if len(listToBeDisplayed) == 0:
            UserInterface.writeLine('no product yet')
        else:
            while True:
                co = UserInterface.displayList('Next action: ',[],'A to check out. B to modify shopping cart Q to quit')
                if co.upper().strip() == 'A':
                    insufficientProduct = self.checkOut()
                    if insufficientProduct != None:
                        for plist in insufficientProduct:
                            proid = plist[0]
                            pro = self.store.getProduct(proid)
                            proName = pro.getName()
                            print("Available stock: ",proName, [plist[1], pro.calculateStock(plist[1])])
                            print("In shopping cart: ",proName, plist[1:])
                        co = UserInterface.displayConfirm('Do you wish to modify shopping cart?','')
                        if co in ['y','Y']:
                            self.modifyShoppingCart()
                    break
                elif co.upper().strip() == 'B':
                    self.modifyShoppingCart()
                    break
                elif co.upper().strip() == 'Q':
                    break
                else:
                    UserInterface.writeLine("Incorrect menu option, try again.")

    def modifyShoppingCart(self):
        while True:
            choice = UserInterface.displayConfirm("Continue? ", "")
            if choice.upper().strip() == 'Y':
                idPrice = UserInterface.displayForm("Please input the product ",[("id","nstring"),("price","money")])
                sc = self.store.getCustomer(self.loginDetail).getShoppingCart()
                # print(idPrice[0])
                acStock = sc.getListByIdPrice(idPrice[0], float(idPrice[1]))
                print(type(idPrice[0]))
                if acStock is not None:
                    newQuan = UserInterface.displayForm("New quantity",[("","money")])[0]
                    print(type(newQuan), float(newQuan))
                    if float(newQuan) == 0.0:
                        sc.deleteFromShoppingCart(idPrice[0],float(idPrice[1]))
                        UserInterface.writeLine("Item deleted from shopping Cart. :\'(")
                    else:
                        acStock[2] = float(newQuan)
                    break
                else:
                    UserInterface.writeLine("Try again. Id and price does not match.")
            else:
                break

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

    def viewAllCustomerID(self):
        toBeDisplayed = []
        customerIds = []
        for customer in self.store.getCustomers():
            id = customer.getId()
            namePhoneAddressBalance = str(customer.getPhoneNumber()) + " " + \
                customer.getAddress() + " " + str(customer.getBalance())
            toBeDisplayed.append((id,namePhoneAddressBalance))
            customerIds.append(id)
        UserInterface.displayList("All customers and their IDs: ", toBeDisplayed, "", False)
        return customerIds

    def viewExpiringProducts(self):
        products = self.store.getProducts()
        paired = []
        expIds = []
        for p in products:
            for b in p.getExpiringBatches():
                paired.append(("Name: {}, Product ID: {}, Batch ID: {}".format(p.getName(), p.getId(), b.getBatchID()),
                    "Expiring: {}".format(b.getExpiryDate())))
                if p.getId() not in expIds:
                    expIds.append(p.getId())
        if len(paired) > 0:
            UserInterface.displayList("Expiring product batches", paired, "", False)
            toDiscount = UserInterface.displayConfirm("Do you wish to discount these products? ", "")
            if toDiscount in ['y','Y']:
                for pid in expIds:
                    self.store.getProduct(pid).updateDiscount()
        else:
            UserInterface.writeLine("Good news! There are no expiring products")

    def browseProducts(self):
        matchingList = self.store.getProducts()
        toBeDisplayed =[("Product Id", ("Name, Unit, Source"))]
        ids = []
        for matchingProduct in matchingList:
            tuple0 = matchingProduct.getId()
            ids.append(tuple0)
            theRest = matchingProduct.getName() + " " + matchingProduct.getUnit() + " " + matchingProduct.getSource()
            newTuple = (tuple0, theRest)
            toBeDisplayed.append(newTuple)
        UserInterface.displayList("The products are: ", toBeDisplayed, "", False)
        while True:
            choice = UserInterface.displayList("View Product? ", [], "Input the product id to view details, Q to quit.")
            if choice.upper() == "Q":
                break
            elif choice in ids:
                self.viewProductByPrice(choice)
                break
            else:
                UserInterface.writeLine("Incorrect product Id")

    def removeCustomer(self):
        idlist = self.viewAllCustomerID()
        validInput = False
        while not validInput:
            customerId = input("Please input customer id, x to quit")
            if customerId in idlist:
                if self.store.getCustomer(customerId).getBalance() > 0:
                    hasconfirmed = False
                    while not hasconfirmed:
                        confirm = UserInterface.displayConfirm("The customer still has some balance, are you sure? ","y or n ")
                        if confirm.lower() == 'y':
                            self.store.removeCustomer(customerId)
                            UserInterface.writeLine("Customer removed.")
                            validInput = True
                            hasconfirmed = True
                        elif confirm.lower() == 'n':
                            UserInterface.writeLine("Cancelled.")
                            hasconfirmed = True
                            validInput = True
                        else:
                            UserInterface.writeLine("Invalid input.")
                else:
                    self.store.removeCustomer(customerId)
                    UserInterface.writeLine("Customer removed.")
                    validInput = True
            elif customerId.upper() == "X":
                validInput = True
            else:
                pass

    def unregisterSelf(self):
        confirm = UserInterface.displayConfirm("Please confirm", "This action will remove your account. Are you sure?")
        if confirm == 'y':
            if self.store.getCustomer(self.loginDetail).getBalance() > 0:
                c2 = UserInterface.displayConfirm("Balance remaining", "You still have balance remaining. Are you sure you want to unregister?")
                if c2 == 'y':
                    self.store.removeCustomer(self.loginDetail)
                    self.loginDetail = None
                    UserInterface.writeLine("Your account has been logged out and unregisted. Thanks for shopping with us!")
                    return
            else:
                self.store.removeCustomer(self.loginDetail)
                self.loginDetail = None
                UserInterface.writeLine("Your account has been logged out and unregisted. Thanks for shopping with us!")
                return

        UserInterface.writeLine("Cancelled.")


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

    # yuki
    # modify the edit product so that it only happens after view
    def editProduct(self, productId):
        attToEdit = True
        while attToEdit is not None:
            UserInterface.writeLine("A. Name  B. Unit C. Source D. Original Price E. Restock F. Deduct Stock Q. Quit ")
            select = UserInterface.displayForm("", [('select:','string')])
            if select[0].upper().strip() == 'Q':
                attToEdit = None
            else:
                if select[0].upper().strip() == 'A':
                    newData = UserInterface.displayForm('input new name:',[('','nstring')])
                    self.store.editProductName(productId, newData[0])
                elif select[0].upper().strip() == 'B':
                    newData = UserInterface.displayForm('input new unit:',[('','nstring')])
                    self.store.editProductUnit(productId, newData[0])
                elif select[0].upper().strip() == 'C':
                    newData = UserInterface.displayForm('input new source:',[('','nstring')])
                    self.store.editProductSource(productId, newData[0])
                elif select[0].upper().strip() == 'D':
                    newData = UserInterface.displayForm('input new price:', [('', 'money')])
                    self.store.editProductOriginalPrice(productId, float(newData[0]))
                elif select[0].upper().strip() == 'E':
                    self.restockProduct(productId)
                elif select[0].upper().strip() == 'F':
                    ap = UserInterface.displayForm("Input the product price to deduct quantity at that price", \
                                                   [("price point: ", "money")])
                    self.reduceProductQuantityByPrice(productId,float(ap[0]))

                attToEdit = True
        # view product after quit the edition
        self.viewProductByPrice(productId)




if __name__ == '__main__':
    s = StoreController()
    while True:
        request = s.displayMenuReturnOption()
        if request == 'A':  # ML
            s.addProduct()
        elif request == 'B':
            s.browseProducts()  # yuki
        elif request == 'S':
            selectP = s.searchProduct()  # yuki
            if selectP is not None:
                s.viewProductByPrice(selectP)
        elif request == 'O':
            s.displayOrderHistory(s.loginDetail)
        elif request == 'R':
            s.register()
        elif request == 'L':
            s.login()
        elif request == 'M':
            s.manageAccount()
        elif request == 'EX':
            s.viewExpiringProducts()
        elif request == 'RC':
            s.removeCustomer()
        elif request == 'RP':
            s.removeProduct()
        elif request == 'SC':
            #viewshoppingcart
            s.viewShoppingCart()
        elif request == 'T':
            s.logout()
        elif request == 'UR':
            s.unregisterSelf()
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