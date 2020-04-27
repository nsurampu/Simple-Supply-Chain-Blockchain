import random

class User:

    '''
    Class implementing the user of the blockchain

    This class primarily deals with the verification of the user using Zero Knowledge
    Proof to verify the transactions against the user ID. It is assumed that the every user
    is an employee associated with the supply chain and carries and employee ID
    '''

    def __init__(self):
        self.id = None
        self.p = None
        self.g = None
        self.r = None
        self.h = None
        self.y = None
        self.b = None
        self.transactions = []

    def generate_y(self):
        self.y = (self.g**self.id) % (self.p)

    def generate_h(self):
        self.r = random.randint(0, self.p-1)
        self.h = (self.g**self.r) % (self.p)

    def generate_s(self):
        return (self.r + self.b*self.id) % (self.p-1)

    def verify_user(self, result):
        if result == (self.h)*(self.y**self.b) % (self.p):
            return True
        else:
            return False

    def view_user(self):
        for transaction in self.transactions:
            print("..." + transaction)
