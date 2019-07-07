""" Provides Verification Methods for the blockchain  """

from  utility.hash_util import hash_string_256, hash_block

class VerificationUtils:
    
    @staticmethod
    def valid_proof(txns, previous_hash, proof):
        guess = (str([tx.get_ordered_dict for tx in txns]) + str(previous_hash) + str(proof)).encode()
        guessed_hash = hash_string_256(guess)
        return guessed_hash[0:2] == '00'
    
    @classmethod
    def verify_chain(cls, blockchain):
        for (index, block )in enumerate(blockchain):    #enumerate returns a tuple of index and element value (index, element)
            if index == 0:
                continue
            prev_hash = block.get_previous_hash()
            calc_hash = hash_block(blockchain[index-1])
            block_txns = block.get_transactions()
            if prev_hash != calc_hash:
                return False
            if not cls.valid_proof(block_txns[:-1],prev_hash,block.get_proof_of_work()):
                print('Invalid Proof of work')
                return False
        return True

    @staticmethod
    def verify_txn(transaction, get_balance):
        sender_balance = get_balance()
        return sender_balance >= transaction.amount
    
    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        return all([cls.verify_txn(tx,get_balance) for tx in open_transactions])