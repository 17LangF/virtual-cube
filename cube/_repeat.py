"""Repeat moves until solved or when the limit is reached."""

from cube.functions import issolved


def repeat(self, *moves: str, limit: int = 1260) -> int:
    """
    Repeat moves until solved or when the limit is reached.

    Parameters
    ----------
    *moves : str
        Sequence of moves.

        If len(`moves`) > 1 and the last argument is an integer or
        numeric string, the integer value is assigned to `limit`.
    limit : int, default=1260
        Maximum number of repetitions of moves.

    Returns
    -------
    int
        Number of repetitions of moves until solved, or 0 if the cube is
        not solved when the `limit` is reached.

    Raises
    ------
    MoveError
        If any of the moves are invalid.

    Notes
    -----
    The default value for `limit` is 1260 as this is the largest number
    of repetitions of a sequence of moves until a 3x3 cube returns to
    its starting state using only face turns. One example of an
    algorithm which will take 1260 repetitions is R U2 D' B D'. If
    non-face turns are used, then 2520 repetitions before returning to
    the starting state is possible. For example, R L2 U' F' Dw.
    """
    if not moves:
        raise TypeError

    if len(moves) > 1:
        if isinstance(moves[-1], int):
            *moves, limit = moves
        elif isinstance(moves[-1], str):
            if moves[-1].isdecimal():
                *moves, limit = moves
                limit = int(limit)

    for i in range(limit):
        self.move(moves)
        if issolved(self.cube):
            return i + 1

    return 0
