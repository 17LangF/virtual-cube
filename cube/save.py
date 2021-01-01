'''
Virtual Cube Program - Made by Fred Lang.
Save and load functions.
'''

from cube import Cube

#Load
def load(filename):
    with open(filename, encoding='utf-8') as file:
        data = file.read().splitlines()

    state, size, moves, smoves, showstyle, colours = data

    cube = Cube()

    size = int(size)
    state = list(state)
    state = [state[y:y + size] for y in range(0, len(state), size)]
    state = [state[s:s + size] for s in range(0, 6 * size, size)]

    cube.cube = state
    cube.size = size
    cube.moves = moves.split()
    cube.smoves = smoves.split()
    cube.showstyle = eval(showstyle)
    cube.colours = eval(colours)

    return cube

#Save
def save(cube, filename):
    attributes = [
        ''.join(x for s in cube.cube for y in s for x in y),
        str(cube.size),
        ' '.join(cube.moves),
        ' '.join(cube.smoves),
        str(cube.showstyle),
        str(cube.colours)
    ]

    with open(filename, 'w', encoding='utf-8') as file:
        file.write('\n'.join(attributes))
