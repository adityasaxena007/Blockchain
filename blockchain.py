import  functools
from utility.hash_util import hash_block
import json
import pickle
from block import Block
from transactions import Transaction
from utility.verification import VerificationUtils

MINING_REWARD = 10
        
class Blockchain:

    def __init__(self,hosting_node_id):
        genesis_block = Block(                                              # first Block of the blockchain
                        previous_hash = '',                                 
                        index = 0,                                  
                        transactions = [],
                        proof = 100,
                        time = 0 
                        )                                                                      
            
        # Initializing our empty blockchain
        self.chain = [genesis_block]
        # UNHANDELED TRANSACTIONS
        self.__open_transactions=[]
        self.hosting_node = hosting_node_id
        self.load_data()

    @property
    def chain(self):
        return self.__chain[:]


    @chain.setter
    def chain(self, value):
        self.__chain = value

    def get_open_txns(self):
        return self.__open_transactions[:]


    def load_data(self):
        try:
            with open('blockchain.p', mode = 'rb') as file:
                data = pickle.loads(file.read())
                temp_chain = []
                for i in data['blockchain']:
                    block_obj = Block(  
                                        i['index'],
                                        i['previous_hash'],
                                        [Transaction(tx['_Transaction__sender'], tx['_Transaction__recipient'], tx['_Transaction__amount']) for tx in i['transactions']],
                                        i['proof'],
                                        i['timestamp']
                                    )
                    temp_chain.append(block_obj)
                
                self.chain = temp_chain

                for i in data['open_txns']:
                    txn = Transaction(  
                                i['_Transaction__sender'],
                                i['_Transaction__recipient'],
                                i['_Transaction__amount'],
                        )
                    self.__open_transactions.append(txn)
        except (IOError, EOFError):
            pass
       

    def save_data(self):
        try:
            with open('blockchain.p',mode='wb') as file:
                data = { 
                    'blockchain': [block.__dict__ for block in [Block( blk.index,
                                                                    blk.previous_hash,
                                                                    [tx.__dict__ for tx in blk.get_transactions()],
                                                                    blk.proof,
                                                                    blk.timestamp) for blk in self.__chain]] ,
                    
                    'open_txns':  [txn.__dict__ for txn in self.__open_transactions]
                }
                file.write(pickle.dumps(data)) 
        except IOError:
            print('SAVING FAILED!!')



    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not (VerificationUtils.valid_proof(txns = self.__open_transactions,previous_hash = last_hash,proof = proof)):
            proof += 1
        return proof



    def get_balance(self):
        participant = self.hosting_node
        tx_sent = [[tx.amount for tx in  block.get_transactions() if tx.sender == participant] for block in self.__chain]     # nested list comprehension
        open_tx_sent = [tx.amount for tx in  self.__open_transactions if tx.sender == participant]
        tx_sent.append(open_tx_sent)

        tx_received = [[tx.amount for tx in  block.get_transactions() if tx.recipient == participant] for block in self.__chain]
        total_amount_sent = 0
        total_amount_rcv = 0

        total_amount_sent = functools.reduce(lambda tx_sum,curr_amt: tx_sum + sum(curr_amt) if len(curr_amt)>0 else tx_sum + 0, tx_sent,0)       #illustrates the USE of lambda function and reduce function
        total_amount_rcv = functools.reduce(lambda tx_sum,curr_amt: tx_sum + sum(curr_amt) if len(curr_amt)>0 else tx_sum + 0, tx_received,0)

        return total_amount_rcv-total_amount_sent

    def get_last_blockchain_val(self):                                                      # Function to get the last element of the blockchain
        """ return the last value of blockchain """
        if (len(self.__chain) < 1):
            return None

        return self.__chain[-1]



    def add_transaction(self, recipient,sender, amount = 1.0):                         #Function to add a transaction
        """ add last blockchain value and a new value to blockchain \n
            Arguments
            sender: sender of amount
            recipient: reciever  of amount
            amount: amount of the transaction
        """

        transaction = Transaction(sender,recipient,amount)

        if VerificationUtils.verify_txn(transaction,self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def mine_block(self):                                                                   #Function to mine blocks (add completed transactions to the blockchain)
        last_block = self.__chain[-1]
        hash_str = hash_block(last_block)
        proof = self.proof_of_work()
        reward_txn = Transaction('Mining', self.hosting_node, MINING_REWARD) 

        copied_txn = self.__open_transactions[:]
        copied_txn.append(reward_txn)
        block = Block(
            previous_hash = hash_str,
            index = len(self.__chain),
            transactions = copied_txn,
            proof = proof 
            )
        self.__chain.append(block)
        self.__open_transactions=[]
        self.save_data()
        return True




