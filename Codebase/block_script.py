import hashlib
import datetime

class Block:

    '''
    Class implementing the basic block of the pharma supply chain blockchain

    Current blocks compute the hash using just the product ID, location ID,
    previous hash and the nonce value of mining for simplicity
    '''

    def __init__(self):
        self.product_id = None
        self.location_id = None
        self.current_hash = None
        self.previous_hash = None
        self.nonce = 0
        self.time = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        self.time_stamp = str(datetime.datetime.now().timestamp() * 1000)
        self.difficulty_hash = 0x00FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        self.difficult_decimal = 452312848583266388373324160190187140051835877600158453279131187530910662655

    def create_block(self, product, location, previous_hash):
        self.previous_hash = previous_hash
        self.product_id = product
        self.location_id = location
        self.current_hash = self.create_hash()

    def create_hash(self):
        hash_str = self.previous_hash + str(self.nonce) + self.product_id + self.location_id
        new_hash = hashlib.sha256(hash_str.encode()).hexdigest()
        return new_hash

    def mine_block(self, miners):
        m = self.current_hash
        while int(m, 16) >= self.difficulty_hash:
            self.nonce += 1
            m = self.create_hash()
            miner = miners[self.nonce % len(miners)]
            self.current_hash = m

        return miner, self.nonce
