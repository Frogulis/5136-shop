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
            newOrder = self.store.addOrder(self.loginDetail, shoppingCart, totalPrice)
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
            # do nothing

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
        newQuantity = int(results[0])
        confirmMsg = UserInterface.displayConfirm("Your new quantity is " + results[0], "Are you sure?")
        if confirmMsg == 'y' or confirmMsg == 'Y':
            self.store.getProduct(productId).getBatch(batchId).setQuantity(newQuantity)
            UserInterface.writeLine("The new quantity is: " + str(newQuantity))
        else:
            UserInterface.writeLine("The action is abandoned.")


    # can only REDUCE quantity by price, adding will cause trouble
    # def reduceProductQuantityByPrice(self, productId, actualPrice):
    #     # TODO
    #     # display old quantity
    #     # ask for new quantity input
    #     newQuantity = pass
    #     self.store.getProduct(productId).deductStock(actualPrice,newQuantity)
    #     #display new quantity


    def login(self):
        # TODO ask for input of userName and password
        self.loginDetail = ""  # should be userId here

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
    #s.searchProduct('ot')
    s.store.addCustomer('cs1','cs1','0450563312','add1')
    s.store.addCustomer('cs2','cs3','0450563312','add1')
    s.store.addCustomer('cs3','cs3','0450563312','add1')
    s.store.addProduct('apple','kg',5, 'China', 10)
    s.store.addProduct('banana', 'kg', 3, 'China', 5)
    s.store.getProduct('1').addBatch(20)
    s.store.getProduct('2').addBatch(30)

    s.editBatchQuantity('1','1')