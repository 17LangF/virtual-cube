"""Iterative deepening A* algorithm."""


def ida_star(self, estimate, next_faces, max_depth=float('inf')):
    """
    Iterative deepening A* algorithm for cubes.

    Finds and executes the shortest sequence of moves from the current
    state of the cube to a state which meets some criteria using a
    heuristic.

    Parameters
    ----------
    estimate : callable
        Function which takes the state of the cube and returns an
        estimate (but never an overestimate) of the number of moves
        required for the cube to meet the criteria, which is used as a
        heuristic. Returns 0 if and only if the cube meets the criteria.
    next_faces : callable
        Function which takes the state of the cube and the moves applied
        and returns a tuple of moves to apply next.
    max_depth : float, default=float('inf')
        Maximum length of sequence of moves to check.

    Returns
    -------
    list or bool
        Moves to solve cube, or False if `max_depth` is exceeded and no
        solution is found.

    Notes
    -----
    Based on `https://en.wikipedia.org/wiki/Iterative_deepening_A*`.
    """
    def search(moves, maximum):
        estimated_length = estimate(self.cube)
        if not estimated_length:
            return True
        estimated_length += len(moves)
        if estimated_length > maximum:
            return estimated_length

        minimum = maximum + 1

        for face in next_faces(self.cube, moves):
            if len(face) == 3:
                face = face[0]
                for turns in '', '2', "'":
                    move = f'{face}{turns}'
                    self.move(face)
                    if turns:
                        self.moves[-2:] = [move]
                    moves.append(move)
                    depth = search(moves, maximum)

                    if depth is True:
                        return True
                    if depth < minimum:
                        minimum = maximum

                    moves.pop()

                self.move(face)
                del self.moves[-2:]

            else:
                for move in face:
                    self.move(move)
                    moves.append(move)
                    depth = search(moves, maximum)

                    if depth == True:
                        return True
                    if depth < minimum:
                        minimum = maximum

                    moves.pop()
                    self.undo()

        return minimum

    maximum = estimate(self.cube)
    moves = []

    while True:
        depth = search(moves, maximum)
        if depth is True:
            return moves
        if depth > max_depth:
            return False
        maximum = depth
