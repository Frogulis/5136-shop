
class ShoppingCart:

    # item = [productId, actualPrice, quantity]
    def __init__(self):
        self.productsInCart = []

    def addToShoppingCart(self, itemToBeAdded):
        self.productsInCart.append(itemToBeAdded)

    def addToShoppingCart(self, productId, actualPrice = 0.00, quantity = 0.00):
        self._convertToFloat(actualPrice)
        self._convertToFloat(quantity)
        newTuple = [productId,actualPrice,quantity]
        self.productsInCart.append(newTuple)

    def adjustQuantity(self, productId, actualPrice = 0.00, newQuantity = 0.00):
        actualPrice = self._convertToFloat(actualPrice)
        newQuantity = self._convertToFloat(newQuantity)
        found = False
        for item in self.productsInCart:
            if item[0] == productId and item[1] == actualPrice:
                item[2] = newQuantity
                found = True
        if not found:
            raise Exception("Either Product Id or Actual Price is invalid.")

    def _convertToFloat(self, integer):
        try:
            floated = round(float(integer), 2)
        except Exception:
            raise Exception("Parameter should be a float or integer.")
        return floated

    def deleteFromShoppingCart(self, itemToBeDeleted):
        for i in range(len(self.productsInCart)):
            if self.productsInCart[i] == itemToBeDeleted:
                del self.productsInCart[i]

    def deleteFromShoppingCart(self, productId, actualPrice = 0.00):
        actualPrice = self._convertToFloat(actualPrice)
        found = False
        for i in range(len(self.productsInCart)):
            item = self.productsInCart[i]
            if item[0] == productId and item[1] == actualPrice:
                del self.productsInCart[i]
                found = True
        if not found:
            raise Exception("Product Id or Actual Price is invalid.")

    # To get one particular product item
    def getProductInCart(self, productId):
        for item in self.productsInCart:
            if productId == item[0]:
                return item
        raise Exception("Product Id is invalid.")

    def getProductsInCart(self):
        return self.productsInCart

    # To get the total price of the shopping cart.
    def getTotalPrice(self):
        totalPrice = 0.00
        for item in self.productsInCart:
            singlePrice = item[1] * item[2]
            totalPrice += singlePrice
        return totalPrice

    def setProductsInCart(self, newList):
        self.productsInCart = newList
