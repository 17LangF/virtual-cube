"""Solve cube in as few moves as possible."""

from .ida_star import ida_star
from cube.functions import issolved, reverse


def optimal_2x2(self) -> tuple:
    """
    Solve 2x2 cube in as few moves as possible.

    Returns
    -------
    tuple of (list of str, dict of {})
        Moves to solve cube, statistics (none).

    Notes
    -----
    All 3674160 permutations of the 2x2 and the optimal moves to reach
    the permutation are listed in `2x2 States and Solutions.txt`.

    Convert the file into a dictionary where each key is the permutation
    and the corresponding value is the list of moves to reach the
    permutation.

    The permutation is represented by a string of 24 characters
    representing the 24 stickers of a 2x2, starting from the U face,
    followed by the L, F, R, B, and D faces, clockwise from the top-left
    sticker of each face.

    The permutation of the cube is converted to its string of 24
    characters. This string is looked up in the dictionary to find the
    optimal solution.

    Solutions are 3-gen, so only use U, F, and R moves.
    """
    if not hasattr(self, 'solutions'):
        with open('docs/2x2 States and Solutions.txt') as f:
            self.solutions = {state: solution for line in f.readlines()
                              for state, solution in [line.split(maxsplit=1)]}

    state = ''.join(''.join(s[0] + s[1][::-1]) for s in self.cube)
    dlb = state[23], state[7], state[18]
    change = {'U': '', 'L': dlb[1], 'F': '', 'R': '', 'B': dlb[2], 'D': dlb[0]}
    faces = 'DLBURF'
    change['U'] = faces[faces.index(change['D']) - 3]
    change['R'] = faces[faces.index(change['L']) - 3]
    change['F'] = faces[faces.index(change['B']) - 3]

    change = {v: k for k, v in change.items()}
    state = ''.join(change[char] for char in state)
    solution = self.solutions[state]
    if solution == '_\n':
        return [], {}

    solve = reverse(solution.split())
    self.move(solve)

    return solve, {}


def optimal_nxn(self) -> tuple:
    """
    Solve cube in as few moves as possible using a brute-force method.

    Returns
    -------
    tuple of (list of str, dict of {})
        Moves to solve cube, statistics (none).

    Notes
    -----
    Brute-force method using `ida_star` to solve the cube. Check every
    possible sequence of moves, iteratively increasing the length of the
    sequence, until the cube is solved.
    """
    size = self.size

    def estimate(cube):
        if issolved(cube):
            return 0
        return 1

    def next_faces(_, moves):
        pure_faces = ['U', 'F', 'R', 'L', 'B', 'D']

        if moves:
            min_depth = 1
            if moves[-1][-1].isalpha():
                index = -1
            else:
                index = -2

            if moves[-1][index] == 'w':
                index -= 1
                min_depth = 2

            face = moves[-1][index]
            if moves[-1][:index]:
                min_depth = int(moves[-1][:index])

            if face in {'L', 'B', 'D'}:
                pure_faces.remove({'L': 'R', 'B': 'F', 'D': 'U'}[face])
        else:
            face = ''
            min_depth = size

        faces = []
        for depth in range(1, size // 2 + 1):
            for pure_face in pure_faces:
                if (pure_face == face and depth <= min_depth or
                    depth == size / 2 and pure_face in {'L', 'B', 'D'}):
                    continue

                if depth == 1:
                    faces.append(pure_face)
                elif depth == 2:
                    faces.append(f'{pure_face}w')
                else:
                    faces.append(f'{depth}{pure_face}w')

        return ((face, f'{face}2', f"{face}'") for face in faces)

    return ida_star(self, estimate, next_faces), {}
