'''
Virtual Cube Program - Made by Fred Lang.
Optimal solver.
'''

#2x2 Optimal
def optimal(self):
    if not hasattr(self, 'solutions'):
        with open('docs/2x2 States and Solutions.txt') as f:
            self.solutions = f.readlines()

    state = ''.join(''.join(s[0] + s[1][::-1]) for s in self.cube)

    DLB = [state[23], state[7], state[18]]
    change = {'U':'','L':DLB[1],'F':'','R':'','B':DLB[2],'D':DLB[0]}
    faces = 'DLBURF'
    change['U'] = faces[faces.index(change['D']) - 3]
    change['R'] = faces[faces.index(change['L']) - 3]
    change['F'] = faces[faces.index(change['B']) - 3]

    change = {v: k for k, v in change.items()}
    state = ''.join(change[char] for char in state)

    for solution in self.solutions:
        if solution.startswith(state):
            solve = self.reverse(solution.split()[1:])
            break
    else:
        return False, {}

    return solve, {}
