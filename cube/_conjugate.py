'''
Virtual Cube Program - Made by Fred Lang.
Conjugate method.
'''

#Conjugate
def conjugate(self, *moves):
    conjugate = ' '.join(moves)
    if conjugate[:1] != '[' or conjugate[-1:] != ']':
        raise TypeError
    conjugate = conjugate[1:-1].split(':')

    if len(conjugate) != 2:
        raise TypeError

    A = conjugate[0].split()
    B = conjugate[1].split()

    conjugate = []

    for move in A + B + self.reverse(A):
        if self.move(move):
            conjugate.append(move)

    return conjugate
