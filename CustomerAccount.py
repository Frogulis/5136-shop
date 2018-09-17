import User
class CustomerAccount(User):
    def __init__(self,phoneNumber, address, shoppingCart):
        self.phoneNumber = phoneNumber
        self.address = address
        self.shoppingCart = shoppingCart
        self.balance = 0