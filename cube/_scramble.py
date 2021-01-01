'''
Virtual Cube Program - Made by Fred Lang.
Scramble method.
'''

import random

from cube.functions import split_move

#Scramble
def scramble(self, *scramble):
    size = self.size
    self.reset(size)

    smoves = []

    if not scramble:
        scramble = ['MOVES']

    #Random moves scrambler
    if scramble[0].upper() == 'MOVES':
        if len(scramble) == 1:
            if size == 2:
                length = 15
            elif size in [0,1,3]:
                length = 25
            else:
                length = 20 * (size - 2)

        elif len(scramble) == 2 and scramble[1].isnumeric():
             length = int(scramble[1])
        else:
            raise TypeError

        invalid_moves = ['', []]

        while len(smoves) < length:
            #0x0 scrambler
            if size == 0:
                smoves = [chr(random.randint(32,255)) for _ in range(length)]
                print(f'SCRAMBLE: {" ".join(smoves)}')
                return False

            #1x1 scrambler
            if size == 1:
                smove = random.choice('xyz')
                if smove in invalid_moves:
                    continue

                invalid_moves[0] = smove

            #2x2+ scrambler
            else:
                if size:
                    depth = random.randint(1,size-1)
                else:
                    depth = 1
                smove = random.choice('UFR')

                if smove == invalid_moves[0]:
                    if depth in invalid_moves[1]:
                        continue
                    invalid_moves[1].append(depth)
                else:
                    invalid_moves = [smove, [depth]]

                if depth > size // 2:
                    depth = size - depth
                    if smove == 'U':
                        smove = 'D'
                    elif smove == 'F':
                        smove = 'B'
                    else:
                        smove = 'L'

                if depth > 1:
                    smove += 'w'
                if depth > 2:
                    smove = str(depth) + smove

            smove += random.choice(('','2',"'"))
            smoves.append(smove)

    #Random state scrambler
    elif scramble[0].upper() == 'STATE':
        #1x1 scrambler
        if size == 1:
            scramble = [random.choice(('','z','x',"z'","x'",'x2'))]
            scramble.append(random.choice(('','y','y2',"y'")))

            if scramble == ['','']:
                scramble = ['x2','y2','z2']

            for smove in scramble:
                if smove:
                    smoves.append(smove)

        #2x2 scrambler
        elif size == 2:
            if not hasattr(self, 'solutions'):
                with open('docs/2x2 States and Solutions.txt') as f:
                    self.solutions = [line.split(maxsplit=1)
                                      for line in f.readlines()]

            smoves = random.choice(self.solutions[1:])[1].split()

        else:
            print('Random state scrambler is not available for this size.')
            return False

    #Input scramble
    else:
        smoves = scramble

    self.move(smoves)
    self.moves = []
    self.smoves = smoves

    return smoves
