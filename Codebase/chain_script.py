import random

class Chain:

    '''
    Class implementing the chaining of the blockchain

    This class in addition to adding blocks, also plays the part of the verifier, to verify
    the user who attempts to add the block to the chain
    '''

    def __init__(self):
        self.blockchain = []

    def add_block(self, block):
        self.blockchain.append(block)

    def verify_chain(self):
        for i in range(1, len(self.blockchain)):
            if self.blockchain[i].previous_hash == self.blockchain[i-1].current_hash:
                continue
            else:
                return False

        return True

    def verify_transaction(self, user):
        user.generate_h()
        user.b = random.randint(0, 1)
        s = user.generate_s()
        result = (user.g**s) % user.p

        return user.verify_user(result)
