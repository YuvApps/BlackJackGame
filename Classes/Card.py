from Classes.Consts import Consts


class Card:
    def __init__(self, suit, name, value, status=1):
        self.suit = suit
        self.name = name
        self.value = value
        self.status = status

    def show(self, tab_counter=1):
        if self.status == Consts.HIDDEN:
            print(tab_counter*4*' ' + "Hidden")
        else:
            print(tab_counter*4*' ' + f"{self.name} of {self.suit}")
