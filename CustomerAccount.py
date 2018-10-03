import UserAccount


class CustomerAccount(UserAccount.UserAccount):
    def __init__(self, ID, password, name, phoneNumber, address, shoppingCart, balance=0, loggedIn=False):
        super(CustomerAccount, self).__init__(ID, name, password, loggedIn)
        self.phoneNumber = phoneNumber
        self.address = address
        self.balance = balance
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
        return "{0:.2f}".format(round(self.balance,2))

    def setBalance(self, newBalance):
        self.balance = round(newBalance,2)

    def getShoppingCart(self):
        return self.shoppingCart

    def setShoppingCart(self, newShoppingCart):
        self.shoppingCart = newShoppingCart

    def topUp(self, enteredAmount):
        self.balance += round(enteredAmount, 2)

    def subtractBalance(self, subtractAmount):
        self.balance -= subtractAmount


if __name__ == '__main__':
    c = CustomerAccount('1234', 'passwd', 'Amy Farah Fowler', '123456789', 'Monash Uni', None, 10, False)

    c.topUp(100.00);
    print (c.getBalance());

