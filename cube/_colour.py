'''
Virtual Cube Program - Made by Fred Lang.
Colour method.
'''

#Colour
def colour(self, side, *colour):
    side = side.upper()
    if side not in ('U','L','F','R','B','D'):
        raise TypeError

    try:
        if len(colour) == 0:
            colours = {
                'U': (255,255,255),
                'L': (255,165,0),
                'F': (0,128,0),
                'R': (255,0,0),
                'B': (0,0,255),
                'D': (255,255,0)
            }
            self.colours[side] = colours[side]
            return

        #HEX
        if len(colour) == 1 and colour[0][0] == '#' and len(colour[0]) == 7:
            colour = tuple(int(colour[0][i:i+2], 16) for i in range(1,7,2))
            self.colours[side] = tuple(colour)
            return

        #RGB
        elif len(colour) == 3 and all(colour[i][-1] == ',' for i in [0,1]):
            colour = colour[0][:-1], colour[1][:-1], colour[2]
            colour = tuple(int(value) for value in colour)
            if all(value < 256 for value in colour):
                self.colours[side] = colour
                return

        raise TypeError

    except ValueError:
        raise TypeError
