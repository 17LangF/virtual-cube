'''
Virtual Cube Program - Made by Fred Lang.
Undo method.
'''

#Undo
def undo(self, number=1):
    if type(number) is str:
        #Undo all
        if number.upper() == 'ALL':
            size = self.size
            self.cube = [[[i]*size for x in range(size)] for i in 'ULFRBD']
            for smove in self.smoves:
                self.move(smove)

            self.moves = []
            return

        #Undo a number of moves
        elif number.isnumeric():
            number = int(number)

        else:
            raise TypeError

    elif not type(number) is int:
        raise TypeError

    for move in self.reverse(self.moves[-number:]):
        self.move(move)

    self.moves = self.moves[:-2*number]
