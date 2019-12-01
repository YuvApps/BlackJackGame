from Classes.Consts import Consts


class Dealer:
    def __init__(self):
        self.cards = []
        self.messages = []
        self.busted = False
        self.stopped = False

    def show_hand(self):
        for card in self.cards:
            card.show()

    def expose_hand(self):
        for card in self.cards:
            card.status = Consts.EXPOSED

    def calc_hand(self):
        counter = 0
        ace_counter = 0
        for card in self.cards:
            if card.name == 'Ace':
                ace_counter += 1
            counter += card.value
        while counter > Consts.BLACKJACK and ace_counter > 0:
            counter -= 10
            ace_counter -= 1
        return counter
