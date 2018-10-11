import UserAccount
from ShoppingCart import ShoppingCart


#yuki: change the order of the parameters between balance and shoppingCart
class CustomerAccount(UserAccount.UserAccount):
    def __init__(self, cid, password, name, phoneNumber, address, balance=0, shoppingCart=None):
        super(CustomerAccount, self).__init__(cid, name, password)
        self.phoneNumber = phoneNumber
        self.address = address
        self.balance = balance
        if shoppingCart == None:
            self.shoppingCart = ShoppingCart()
        else:
            self.shoppingCart = shoppingCart

    def getPhoneNumber(self):
        return self.phoneNumber

    def setPhoneNumber(self, newPhoneNumber):
        self.phoneNumber = newPhoneNumber

    def getAddress(self):
        return self.address

    def setAddress(self, newAddress):
        self.address = newAddress

    def getBalance(self):
        return self.balance

    def setBalance(self, newBalance):
        self.balance = round(newBalance, 2)

    def getShoppingCart(self):
        return self.shoppingCart

    def setShoppingCart(self, newShoppingCart):
        self.shoppingCart = newShoppingCart

    def topUp(self, enteredAmount):
        self.balance += round(float(enteredAmount), 2)
        return self.balance

    def subtractBalance(self, subtractAmount):
        if self.balance - subtractAmount >= 0:
            self.balance -= subtractAmount
        else:
            raise Exception("Insufficient Funds")


if __name__ == '__main__':
    pass#c = CustomerAccount('1234', 'passwd', 'Amy Farah Fowler', '123456789', 'Monash Uni')
#c.getName()
