import random

class Miners:

    '''
    Class implemeting the miners for mining the blocks

    This class can be used to create new miners with various computing power and
    build a miners network
    '''

    def __init__(self):
        self.miners = []
        self.cpus = []
        self.miner_info = {}

    def add_miner(self, user, cpu_units):
        self.miner_info[user] = cpu_units
        self.cpus.append(cpu_units * [user])

    def create_miner_network(self):
        for cpu in self.cpus:
            self.miners.extend(cpu)

        random.shuffle(self.miners)
