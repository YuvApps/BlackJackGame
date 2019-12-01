from Classes.Dealer import Dealer
from Classes.Deck import Deck
from Classes.Consts import Consts


class OnePlay:
    def __init__(self, players):
        self.players = players
        self.init_players()
        self.dealer = Dealer()
        self.deck = Deck()
        self.deck.shuffle()
        self.max_lig_bet = 0
        self.active_players = len(players) + 1

    def init_players(self):
        for player in self.players:
            for hand in player.hands:
                hand.indexes.lose = False
                hand.indexes.win = False
                hand.indexes.finish = False
                hand.indexes.equal = False
                hand.cards = []
                hand.messages = []

    def make_a_round(self):
        for cards in range(1, 3):
            for player in self.players:
                hand_index = -1
                for hand in player.hands:
                    hand_index += 1
                    if len(hand.cards) == 0:
                        bet = int(input(f"{player.name}, please place your bet: "))
                        while not self.check_bet(player, bet):
                            print(f"Sorry {player.name}, your bet is illegal")
                            bet = int(input(f"{player.name}, please place your bet: "))
                        hand.bet = bet
                        player.balance -= hand.bet
                    hand.cards.append(self.deck.draw_card())

            self.dealer.cards.append(self.deck.draw_card())
            if len(self.dealer.cards) == 1:
                self.dealer.cards[0].status = Consts.HIDDEN

        print('\n'*80)
        print(f"The Table's Status now is: ")
        self.show()

        for player in self.players:
            hand_index = -1
            for hand in player.hands:
                hand_index += 1
                while not (hand.indexes.lose
                           or hand.indexes.finish):
                    print(f"{player.name}'s Turn: ")
                    self.make_player_move(player, player.play(hand_index), hand_index)
                    self.check_player(player, hand_index)
                    print('\n' * 80)
                    print(f"The Table's Status now is: ")
                    self.show()

            while not (self.dealer.busted or self.dealer.stopped):
                self.make_dealer_move()

            print('\n' * 80)
            print(f"The Table's Status now is: ")
            self.show()

    def check_bet(self, player_index, bet):
        if bet == 0 or bet > self.players[player_index].balance:
            return False
        return True

    def make_player_move(self, player, player_action, hand_index):
        if player_action == Consts.ACTION_DRAW:
            player.hands[hand_index].cards.append(self.deck.draw_card())
            print(f"{player.name} has decided to hit")
            if player.calc_hand(hand_index) == Consts.BLACKJACK:
                player.hands[hand_index].indexes.finish = True
                msg = f"{player.name} have reached BlackJack!"
                player.hands[hand_index].messages.append(msg)
                print(msg)
                self.active_players -= 1
        elif player_action == Consts.ACTION_STAY:
            player.hands[hand_index].indexes.finish = True
            print(f"{player.name} has decided to stay")
            self.active_players -= 1
        elif player_action == Consts.ACTION_DOUBLE_DOWN:
            pass
        elif player_action == Consts.ACTION_SPLIT:
            pass
        elif player_action == Consts.ACTION_SURRENDER:
            pass
        elif player_action == Consts.ACTION_INSURANCE:
            pass
        pass

    def make_dealer_move(self):
        if self.dealer.cards[0].status == Consts.HIDDEN:
            self.dealer.expose_hand()
        else:
            if self.dealer.calc_hand() < Consts.DEALER_STOPPER and self.dealer.calc_hand() <= self.max_lig_bet:
                self.dealer.cards.append(self.deck.draw_card())
            else:
                if self.dealer.calc_hand() > Consts.BLACKJACK:
                    msg = "The dealer has been BUSTED"
                    self.dealer.messages.append(msg)
                    print(msg)
                    self.dealer.busted = True
                else:
                    msg = "The dealer can't draw anymore."
                    self.dealer.messages.append(msg)
                    print(msg)
                    self.dealer.stopped = True

                self.active_players -= 1
                self.update_all_winners(self.dealer.calc_hand())

    def update_all_winners(self, dealer_hand):
        for player in self.players:
            for hand in player.hands:
                if not hand.indexes.lose:
                    if Consts.BLACKJACK >= hand.calc_hand() > dealer_hand \
                            or (hand.calc_hand() < dealer_hand and dealer_hand > Consts.BLACKJACK > hand.calc_hand()):
                        msg = f"{player.name} won the dealer!"
                        hand.messages.append(msg)
                        print(msg)
                        hand.indexes.win = True
                    elif hand.calc_hand() == dealer_hand:
                        msg = f"{player.name} is equal to the dealer!"
                        hand.messages.append(msg)
                        print(msg)
                        hand.indexes.equal = True
                    elif hand.calc_hand() < dealer_hand <= Consts.BLACKJACK or hand.calc_hand() > Consts.BLACKJACK:
                        msg = f"{player.name} lose the dealer!"
                        hand.messages.append(msg)
                        print(msg)
                        hand.indexes.lose = True

    def check_player(self, player, hand_index):
        if player.calc_hand(hand_index) > 21:
            msg = f"{player.name} have been BUSTED!"
            player.hands[hand_index].messages.append(msg)
            print(msg)
            player.hands[hand_index].indexes.lose = True
            self.active_players -= 1
        elif self.max_lig_bet < player.calc_hand(hand_index):
            self.max_lig_bet = player.calc_hand(hand_index)

    def show(self):
        for player in self.players:
            hand_index = -1
            print(f"{player.name}'s status is:")
            for hand in player.hands:
                hand_index += 1
                if not hand:
                    print(f"\t{player.name} has no cards yet..")
                else:
                    if len(player.hands) > 1:
                        print(f"\tThe {hand_index}'s hand of {player.name} is:")
                    else:
                        print(f"\t{player.name}'s hand is: ")
                    player.show_hand(hand_index, 2)
                    print()
                    print(f"\t{player.name}'s hand sum is: {player.calc_hand(hand_index)}")
                print(f"\t{player.name}'s bet for this round is: {hand.bet}")
                for msg in hand.messages:
                    print("\t" + msg)
            print(f"\t{player.name}'s current balance is: {player.balance}")
            print()

        print(f"The dealer's status is:")
        if not self.dealer.cards:
            print("\tThe dealer has no cards yet..")
        else:
            print(f"\tThe dealer has the cards: ")
            self.dealer.show_hand(1)
            print()
        if self.dealer.cards[0].status == Consts.EXPOSED:
            print(f"\tThe dealer's hand sum is: {self.dealer.calc_hand()}")
        for msg in self.dealer.messages:
            print(msg)
