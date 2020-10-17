'''
Virtual Cube Program - Made by Fred Lang.
Reverse method.
'''

from cube.functions import split_move

#Reverse
def reverse(self, *moves):
    if not moves:
        moves = self.moves
    elif len(moves) == 1:
        moves = moves[0]

    reverse = []
    for move in moves[::-1]:
        if not split_move(move, self.size):
            print(f'{move} is invalid.')
            continue

        if move[-1] == "'":
            reverse.append(move[:-1])
        elif move[-1] == '2':
            reverse.append(move)
        else:
            reverse.append(move + "'")

    return reverse
