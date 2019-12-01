from Classes.OnePlay import OnePlay
from copy import deepcopy


class Table:
    def __init__(self):
        self.players = []

    def show(self):
        for player in self.players:
            print(f"{player.name}'s current balance is: {player.balance}")

    def start_game(self, players):
        start = input("Can We Start The Game? 1(Yes)/2(No) ")
        while start == '1':
            self.players = deepcopy(players)
            while self.players:
                main_one_play = OnePlay(deepcopy(self.players))
                while main_one_play.active_players > 0:
                    main_one_play.make_a_round()
                self.update_winners_losers(main_one_play)
            start = input("Start Again? 0(Restart from beginning)/ 1(Rematch with same initiatives)/ 2(No Thanks) ")

    def update_winners_losers(self, one_play):
        player_index = -1
        for player in one_play.players:
            player_index += 1
            hand_index = -1
            for hand in player.hands:
                hand_index += 1
                if hand.indexes.win:
                    self.players[player_index].balance += hand.bet * 2
                elif hand.indexes.equal:
                    self.players[player_index].balance += hand.bet
                else:
                    self.players[player_index].balance -= hand.bet

            if self.players[player_index].balance > 0 \
                    and self.players[player_index].balance >= self.players[player_index].init_bet:
                answer = int(input(f"{self.players[player_index].name}, "
                                   f"Your balance is: {self.players[player_index].balance}."
                                   f" Do You wish to continue to another round? 1(Yes)/2(No): "))
                if answer == 2:
                    self.remove_by_name(player.name)
            else:
                print(f"Sorry {self.players[player_index].name}, you are out of money.. Bye Bye :)")
                self.remove_by_name(player.name)

    def remove_by_name(self, name):
        for player in self.players:
            if player.name == name:
                self.players.remove(player)
