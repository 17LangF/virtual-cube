'''
Virtual Cube Program - Made by Fred Lang.
Commutator method.
'''

#Commutator
def commutator(self, *moves):
    commutator = ' '.join(moves)

    if commutator[:1] != '[' or commutator[-1:] != ']':
        raise TypeError

    commutator = commutator[1:-1].split(',')

    if len(commutator) != 2:
        raise TypeError

    A = commutator[0].split()
    B = commutator[1].split()

    if not (A and B):
        raise TypeError

    commutator = []

    for move in A + B + self.reverse(A) + self.reverse(B):
        if self.move(move):
            commutator.append(move)

    return commutator
