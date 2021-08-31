"""Reverse last move or last number of moves."""

from cube.functions import reverse


def undo(self, number=1):
    """
    Reverse last move or last number of moves.

    Parameters
    ----------
    number : str or int, default=1
        Number of moves to undo.

        If `number` == 'ALL', then all moves are reversed.

        Else, `number` must be an integer or numeric string.
    """
    if isinstance(number, str):
        # Undo all
        if number.upper() == 'ALL':
            smoves = self.smoves
            self.reset(self.size)
            self.smoves = smoves
            self.move(smoves)
            self.moves = []
            return
        # Undo a number of moves
        elif number.isdecimal():
            number = int(number)
        else:
            raise ValueError

    self.move(reverse(self.moves[-number:]))
    self.moves = self.moves[:-2*number]
