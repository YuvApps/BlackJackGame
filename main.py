from Classes.Table import Table
from Classes.Player import Player


def main():
    start = '0'
    print("Welcome to The Great Blackjack Game!")

    while start == '0':
        players = []
        players_amount = int(input("How many players are you? "))

        for index in range(1, players_amount + 1):
            given_name = input(f"Player No. {index}, What is your name? ")
            balance_amount = int(input("How much you want to start your balance? "))
            players.append(Player(given_name, balance_amount))

        main_table = Table()

        main_table.start_game(players)

        print("Thanks for being part of this great game..")


main()
