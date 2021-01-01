'''
Virtual Cube Program - Made by Fred Lang.
Optimal solver.
'''

from cube.functions import reverse

#2x2 Optimal
def optimal(self):
    if not hasattr(self, 'solutions'):
        with open('docs/2x2 States and Solutions.txt') as f:
            self.solutions = [line.split(maxsplit=1) for line in f.readlines()]

    state = ''.join(''.join(s[0] + s[1][::-1]) for s in self.cube)

    dlb = [state[23], state[7], state[18]]
    change = {'U':'','L':dlb[1],'F':'','R':'','B':dlb[2],'D':dlb[0]}
    faces = 'DLBURF'
    change['U'] = faces[faces.index(change['D']) - 3]
    change['R'] = faces[faces.index(change['L']) - 3]
    change['F'] = faces[faces.index(change['B']) - 3]

    change = {v: k for k, v in change.items()}
    state = ''.join(change[char] for char in state)

    for possible_state, solution in self.solutions:
        if possible_state == state:
            if solution == '_\n':
                solve = []
            else:
                solve = reverse(solution.split())
            break
    else:
        return False, {}

    self.move(solve)

    return solve, {}
