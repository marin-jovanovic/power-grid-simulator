"""
utils for address translations
"""


class Address:

    @staticmethod
    def get_as_csv(asdu_address, io_address):
        return str(asdu_address) + ";" + str(io_address)

    def __init__(self, asdu_address, io_address):
        self.asdu_address = asdu_address
        self.io_address = io_address

    def __str__(self):
        return f"{self.asdu_address=} {self.io_address=}"

    def formatted_name(self):
        return Address.get_as_csv(self.asdu_address, self.io_address)
