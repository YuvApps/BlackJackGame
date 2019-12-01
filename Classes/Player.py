from Classes.Consts import Consts


class Indexes:
    def __init__(self):
        self.finish = False
        self.lose = False
        self.win = False
        self.equal = False


class Hand:
    def __init__(self):
        self.cards = []
        self.indexes = Indexes()
        self.bet = 0
        self.messages = []

    def calc_hand(self):
        counter = 0
        for card in self.cards:
            counter += card.value
        return counter


class Player:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.hands = []
        hand = Hand()
        self.hands.append(hand)

    def show_hands(self):
        index = 0
        for _ in self.hands:
            index += 1
            if len(self.hands) > 1:
                print(f"{self.name}'s Hand No. {index} is: ")
            else:
                print(f"{self.name}'s Hand is: ")

            self.show_hand(index, 1)

    def show_hand(self, hand_index, tab_counter):
        for card in self.hands[hand_index].cards:
            card.show(tab_counter)

    def calc_hand(self, hand_index):
        counter = 0
        ace_counter = 0
        for card in self.hands[hand_index].cards:
            if card.name == 'Ace':
                ace_counter += 1
            counter += card.value
        while counter > Consts.BLACKJACK and ace_counter > 0:
            counter -= 10
            ace_counter -= 1
        return counter

    def play(self, hand_index):
        act_msg = f'What do you want to do? ' \
                  f'{f"{Consts.ACTION_DRAW}(Hit)/" if self.chk_act(Consts.ACTION_DRAW) else ""}' \
                  f'{f"{Consts.ACTION_STAY}(Stand)" if self.chk_act(Consts.ACTION_STAY) else ""}' \
                  f'{f"/{Consts.ACTION_DOUBLE_DOWN}(Double Down)" if self.chk_act(Consts.ACTION_DOUBLE_DOWN) else ""}' \
                  f'{f"/{Consts.ACTION_SPLIT}(Split)" if self.chk_act(Consts.ACTION_SPLIT) else ""}' \
                  f'{f"/{Consts.ACTION_SURRENDER}(Surrender)" if self.chk_act(Consts.ACTION_SURRENDER) else ""}' \
                  f'{f"/{Consts.ACTION_INSURANCE}(Insurance)" if self.chk_act(Consts.ACTION_INSURANCE) else ""}' \
                  f' : '
        action = int(input(act_msg))
        while not self.check_if_possible(action, hand_index):
            action = int(input(act_msg))
        return action

    def chk_act(self, action):
        if action == Consts.ACTION_DRAW:
            for hand in self.hands:
                if hand.calc_hand() < Consts.BLACKJACK:
                    return True
        elif action == Consts.ACTION_STAY:
            return True
        else:
            return False

    def check_if_possible(self, action, hand_index):
        if not self.hands[hand_index].indexes.lose and action > Consts.ACTION_STAY:
            return False
        return True
