from Classes.Card import Card
import random


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for suit in ["Spades", "Clubs", "Diamonds", "Hearts"]:
            for value in range(1, 14):
                if value == 1:
                    value = 11
                    name = "Ace"
                elif value == 11:
                    value = 10
                    name = "Jack"
                elif value == 12:
                    value = 10
                    name = "Queen"
                elif value == 13:
                    value = 10
                    name = "King"
                else:
                    name = value
                self.cards.append(Card(suit, name, value))

    def show(self):
        for card in self.cards:
            card.show()

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def draw_card(self):
        if len(self.cards) == 1:
            card = self.cards.pop()
            self.cards = Deck()
        else:
            card = self.cards.pop()
        return card
