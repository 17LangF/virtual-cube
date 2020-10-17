'''
Virtual Cube Program - Made by Fred Lang.
Scramble method.
'''

import random

#Scramble
def scramble(self, *scramble):
    size = self.size
    self.reset(size)

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

        while len(self.smoves) < length:
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
            self.move(smove)
            self.smoves.append(smove)
            self.moves.pop()

    #Random state scrambler
    elif scramble[0].upper() == 'STATE':
        if size == 1:
            scramble = [random.choice(('','z','x',"z'","x'",'x2'))]
            scramble.append(random.choice(('','y','y2',"y'")))

            if scramble == ['','']:
                scramble = ['x2','y2','z2']

            for smove in scramble:
                if smove:
                    self.move(smove)
                    self.smoves.append(smove)
                    self.moves.pop()

        elif size == 2:
            if not hasattr(self, 'solutions'):
                with open('docs/2x2 States and Solutions.txt') as f:
                    self.solutions = f.readlines()[1:]

            for smove in random.choice(self.solutions).split()[1:]:
                self.move(smove)
                self.smoves.append(smove)
                self.moves.pop()

        else:
            print('Random state scrambler is not available for this size.')

    #Input scramble
    else:
        for smove in scramble:
            if self.move(smove):
                self.smoves.append(smove)
                self.moves.pop()
            else:
                print(f'{smove} is invalid.')

    return self.smoves
