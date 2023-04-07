import time
from game import *
from colorama import Cursor, Fore, Style

class Player:
    def play(game: Game, opts: dict):
        pass

class Human(Player):
    def play(game: Game, opts: None) -> Game:
        print(game)
        print("Move: ", end="")

        try:
            move = int(input())
            game = game.move(move)
        except Exception:
            pass

        return game

game = TicTacToe("         ")

while game.getStatus() == Status.playing:
    game = Human.play(game, None)

    if game.getStatus() == Status.playing:
        game = Human.play(game, None)

print(game)
print("Game over: ", end="")
if game.getStatus() == Status.draw:
    print("Draw")
else:
    print(f"{game.winner} won")
