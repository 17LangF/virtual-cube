'''
Virtual Cube Program - Made by Fred Lang.
Undo method.
'''

from cube.functions import reverse

#Undo
def undo(self, number=1):
    if isinstance(number, str):
        #Undo all
        if number.upper() == 'ALL':
            smoves = self.smoves
            self.reset(self.size)

            self.smoves = smoves
            self.move(smoves)
            self.moves = []
            return

        #Undo a number of moves
        elif number.isnumeric():
            number = int(number)

        else:
            raise TypeError

    elif not isinstance(number, int):
        raise TypeError

    self.move(reverse(self.moves[-number:]))
    self.moves = self.moves[:-2*number]
