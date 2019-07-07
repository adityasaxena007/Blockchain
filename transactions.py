from collections import OrderedDict
from utility.printable import Printable

class Transaction(Printable):
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    @property
    def sender(self):
        return self.__sender

    @sender.setter
    def sender(self,value):
        self.__sender = value

    @property
    def recipient(self):
        return self.__recipient

    @recipient.setter
    def recipient(self,value):
        self.__recipient = value

    
    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self,value):
        self.__amount = value


    def get_ordered_dict(self):
        return  OrderedDict(
                [('sender', self.sender),
                ('recipient', self.recipient),
                ('amount', self.amount)
                ]
        )