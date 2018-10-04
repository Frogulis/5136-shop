
class ShoppingCart:

    # tuple = (productId, actualPrice, quantity)
    def __init__(self):
        self.productsInCart = []

    def addToShoppingCart(self, tupleToBeAdded):
        self.productsInCart.append(tupleToBeAdded)

    def addToShoppingCart(self, productId, actualPrice = 0.00, quantity = 0.00):
        self._convertToFloat(actualPrice)
        self._convertToFloat(quantity)
        newTuple = (productId,actualPrice,quantity)
        self.productsInCart.append(newTuple)

    def adjustQuantity(self, productId, actualPrice = 0.00, newQuantity = 0.00):
        actualPrice = self._convertToFloat(actualPrice)
        newQuantity = self._convertToFloat(newQuantity)
        for tuple in self.productsInCart:
            if tuple[0] == productId and tuple[1] == actualPrice:
                tuple[2] = newQuantity
            raise Exception("Either Product Id or Actual Price is invalid.")

    def _convertToFloat(self, integer):
        try:
            floated = round(float(integer), 2)
        except Exception:
            raise Exception("Parameter should be a float or integer.")
        return floated

    def deleteFromShoppingCart(self, tupleToBeDeleted):
        del self.productsInCart[tupleToBeDeleted]

    def deleteFromShoppingCart(self, productId, actualPrice = 0.00):
        actualPrice = self._convertToFloat(actualPrice)
        for tuple in self.productsInCart:
            if tuple[0] == productId and tuple[1] == actualPrice:
                del self.productsInCart[tuple]
            else:
                raise Exception("Product Id or Actual Price is invalid.")

    # To get one particular product tuple
    def getProductInCart(self, productId):
        for tuple in self.productsInCart:
            if productId == tuple[0]:
                return tuple
            raise Exception("Product Id is invalid.")

    def getProductsInCart(self):
        return self.productsInCart

    # To get the total price of the shopping cart.
    def getTotalPrice(self):
        totalPrice = 0.00
        for tuple in self.productsInCart:
            singlePrice = tuple[1] * tuple[2]
            totalPrice += singlePrice
        return totalPrice

    def setProductsInCart(self,newTuple):
        self.productsInCart = newTuple
