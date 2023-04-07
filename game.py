import os
import abc
from enum import Enum
from colorama import Fore, Style
from typing import Iterator, TypeVar

class Status(Enum):
    playing = 0
    draw = 1
    won = 2

T = TypeVar('T', bound='Game')

class Game(abc.ABC):
    bits = None

    @abc.abstractmethod
    def __init__(self, state):
        pass

    @abc.abstractmethod
    def __str__(self) -> str:
        pass

    @abc.abstractmethod
    def __iter__(self) -> Iterator[T]:
        pass

    @abc.abstractmethod
    def getStatus(self) -> Status:
        pass

    @abc.abstractmethod
    def move(self, move: str) -> T:
        pass

    @abc.abstractmethod
    def encode(self) -> int:
        pass

    @abc.abstractmethod
    def decode(state: int) -> str:
        pass

U = TypeVar('U', bound='TicTacToe')

class TicTacToe(Game):
    bits = 19
    winner = None

    def __init__(self, state):
        if type(state) is int:
            self.state = self.decode(state)
        elif type(state) is str:
            if len(state) != 9:
                raise ValueError(f"Invalid state: expected 9 characters, got {len(state)}")

            if not all([c in " XO" for c in state]):
                raise ValueError(f"Invalid state: expected only 'X', 'O' or ' ', got {state}")

            if state.count("X") - state.count("O") not in [0, 1]:
                raise ValueError(f"Invalid state: expected # of X's - # of O's to be 0 or 1, got {state.count('X') - state.count('O')}")

            self.state = state
        else:
            raise TypeError(f"Invalid state: expected str or int, got {type(state)}")

        self.next = "X" if self.state.count("X") == self.state.count("O") else "O"

    def __str__(self) -> str:
        board = ""
        for i in range(9):
            if self.state[i] == " ":
                board += f"{Style.DIM} {i} {Style.RESET_ALL}"
            else:
                board += f"{Style.BRIGHT}{Fore.GREEN} {self.state[i]} {Style.RESET_ALL}"

            if i % 3 != 2:
                board += f"{Style.BRIGHT}|{Style.RESET_ALL}"

            if i % 3 == 2 and i != 8:
                board += f"\n{Style.BRIGHT}---|---|---{Style.RESET_ALL}\n"
        return board
        """
        return f" {self.state[0]} | {self.state[1]} | {self.state[2]} \n" \
            "---|---|---\n" \
            f" {self.state[3]} | {self.state[4]} | {self.state[5]} \n" \
            "---|---|---\n" \
            f" {self.state[6]} | {self.state[7]} | {self.state[8]} \n"
        """

    def __iter__(self) -> Iterator[U]:
        return iter([self.move(i) for i in range(9) if self.state[i] == " "])

    def move(self, move: str) -> U:
        move = int(move)

        if self.state[move] != " ":
            raise Exception("Invalid move")
        else:
            new_state = self.state[:move] + self.next + self.state[move+1:]
            return TicTacToe(new_state)

    def getStatus(self) -> Status:
        for i in range(3):
            if self.state[3*i] == self.state[3*i+1] == self.state[3*i+2] != " ":
                self.winner = self.state[3*i]
                return Status.won
            if self.state[i] == self.state[i+3] == self.state[i+6] != " ":
                self.winner = self.state[i]
                return Status.won

        if self.state[0] == self.state[4] == self.state[8] != " ":
            self.winner = self.state[0]
            return Status.won
        if self.state[2] == self.state[4] == self.state[6] != " ":
            self.winner = self.state[2]
            return Status.won

        if " " not in self.state:
            return Status.draw

        return Status.playing

    """
    Encoding format:
        9 bits for each square: 0 = empty, 1 = occupied
        9 bits for each square: 0 = O, 1 = X
        1 bit for next player: 0 = O, 1 = X

    Example:
         O |   | X
        ---|---|---
         X |   | O
        ---|---|---
         X | O | X

         Would be encoded as:

         0b101_101_111_001_100_101_0
    """
    def encode(self) -> int:
        encoding = 0

        for i in range(9):
            encoding |= 1 if self.state[i] != " " else 0
            encoding <<= 1

        for i in range(9):
            encoding |= 1 if self.state[i] == "X" else 0
            encoding <<= 1

        encoding |= 1 if self.next == "X" else 0

        return encoding

    def decode(state: int) -> str:
        state = bin(state)[2:]

        new_state = ""
        for i in range(9):
            if state[i] == "0":
                new_state += " "
            else:
                new_state += "X" if state[i+9] == "1" else "O"

        return new_state
