from utility.verification import VerificationUtils
from blockchain import Blockchain
from uuid import uuid4
class Node:
    def __init__(self):
        #self.id = str(uuid4())
        self.id = 'aditya'
        self.blockchain = Blockchain(self.id)


    def get_txn_value(self):                                                                #Function to get the transaction value(recepient and the amount)
        tx_recipient = input('Enter the  recipient : ')
        tx_amount =  float(input('your transaction amount : '))
        return (tx_recipient,tx_amount)


    def get_user_choice(self):
        user_input = input('your choice: ')
        return user_input


    def print_blockchain_element(self):                                                     #Function to print the blockchain
        for i in self.blockchain.chain:
            print('Outputing block')
            print(i)


    def listen_for_input(self):
        while True:
            print('Please Choose')
            print('1: Add new transaction Value')
            print('2: Output the Blockchain')
            print('3: Mine a new block')
            print('4: Verify Transactions')
            print('q: Quit')
            user_choice = self.get_user_choice()

            if user_choice == '1':
                tx_data = self.get_txn_value()
                recipient, amount = tx_data
                if self.blockchain.add_transaction(recipient = recipient,sender = self.id, amount = amount):
                    print('Trasaction Successful')
                else:
                    print('Trasaction Failed')
            elif user_choice == '2':
                # Output individual blocks
                self.print_blockchain_element()
            elif user_choice == '3':
                self.blockchain.mine_block()
            elif user_choice == '4':
                if VerificationUtils.verify_transactions(self.blockchain.get_open_txns(),self.blockchain.get_balance):
                    print("All Transactions are valid")
                else:
                    print("There are Invalid Transactions ")
            elif user_choice == 'q':
                break
            else:
                print('Input was invalid , Please pick a value from the list')

            print('Balance of {} is : {:6.2f} '.format(self.id,self.blockchain.get_balance( )))

            if not VerificationUtils.verify_chain(self.blockchain.chain):
                print('Invalid Blockchain')
                break
        else:
            print('User Left')
        print('Done!')

if __name__ == '__main__':
    node = Node()
    node.listen_for_input()