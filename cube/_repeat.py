'''
Virtual Cube Program - Made by Fred Lang.
Repeat method.
'''

from cube.functions import issolved, split_move

#Repeat
def repeat(self, *moves):
    if not moves:
        raise TypeError

    limit = 1260

    if len(moves) > 1:
        if isinstance(moves[-1], int):
            limit = moves[-1]
            moves = moves[:-1]

        elif isinstance(moves[-1], str):
            if moves[-1].isnumeric():
                limit = int(moves[-1])
                moves = moves[:-1]

    for i in range(limit):
        self.move(moves)

        if issolved(self.cube):
            return i + 1

    return False
