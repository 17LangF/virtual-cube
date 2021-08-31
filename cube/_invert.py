"""Switch to the inverse scramble and reverse moves."""

from cube.functions import reverse


def invert(self):
    """Switch to the inverse scramble and reverse moves."""
    smoves = self.smoves
    moves = self.moves
    self.reset(self.size)
    self.smoves = reverse(moves)
    self.move(self.smoves)
    self.moves = []
    self.move(reverse(smoves))
