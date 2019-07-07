from time import time
from utility.printable import Printable

class Block(Printable):
    def __init__(self, index, previous_hash, transactions, proof, time=time()):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.proof = proof
        self.timestamp = time
    
    def get_index(self):
        return self.index

    def get_previous_hash(self):
        return self.previous_hash

    def get_transactions(self):
        return self.transactions

    def get_proof_of_work(self):
        return self.proof