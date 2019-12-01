from Classes.Consts import Consts


class Card:
    def __init__(self, suit, name, value, status=1):
        self.suit = suit
        self.name = name
        self.value = value
        self.status = status

    def show(self):
        if self.status == Consts.HIDDEN:
            print("Hidden")
        else:
            print(f"{self.name} of {self.suit}")
