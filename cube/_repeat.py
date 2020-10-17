'''
Virtual Cube Program - Made by Fred Lang.
Repeat method.
'''

from cube.functions import issolved, split_move

#Repeat
def repeat(self, *moves):
    if not moves:
        raise TypeError

    if type(moves[-1]) is int:
        limit = moves[-1]
        moves = moves[:-1]
    elif type(moves[-1]) is str:
        if moves[-1].isnumeric():
            limit = int(moves[-1])
            moves = moves[:-1]
        else:
            limit = 1000
    else:
        raise TypeError

    for move in moves:
        if not split_move(move, self.size):
            print(f'{move} is invalid.')
            index = moves.index(move)
            moves = moves[:index] + moves[index + 1:]

    for i in range(limit):
        for move in moves:
            self.move(move)
        if issolved(self.cube):
            break

    return i + 1
