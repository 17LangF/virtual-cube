"""Change the colour of a side of the cube."""


def colour(self, side: str, colour: str = None):
    """
    Change the colour of a side of the cube.

    Parameters
    ----------
    side : {'U', 'L', 'F', 'R', 'B', 'D'}
        Single character which represents one side of the cube.
    colour : str, optional
        Colour given as R,G,B (RGB code), #RRGGBB (HEX code), or named
        colour. If `colour` is None, the default colour for the given
        side is used.

        The default colours for each side are:
            U: #ffffff or 255,255,255 or white
            L: #ffa500 or 255,165,0 or orange
            F: #008000 or 0,128,0 or green
            R: #ff0000 or 255,0,0 or red
            B: #0000ff or 0,0,255 or blue
            D: #ffff00 or 255,255,0 or yellow

        The allowed named colours are:
            white: 255,255,255
            black: 0,0,0
            red: 255,0,0
            orange: 255,165,0
            yellow: 255,255,0
            green: 0,128,0
            blue: 0,0,255
            purple: 128,0,128
            magenta: 255,0,255
            pink: 255,192,203
            cyan: 0,255,255
            brown: 165,42,42
            grey: 128,128,128
            gray: 128,128,128

    Raises
    ------
    ValueError
        If side is not one of U, L, F, R, B, D or if colour cannot be
        interpreted or is not recognised.
    """
    side = side.upper()
    if side not in {'U', 'L', 'F', 'R', 'B', 'D'}:
        raise ValueError

    # Default colours
    if not colour:
        colours = {
            'U': (255,255,255),
            'L': (255,165,0),
            'F': (0,128,0),
            'R': (255,0,0),
            'B': (0,0,255),
            'D': (255,255,0)
        }
        self.colours[side] = colours[side]

    # HEX colours
    elif colour.startswith('#') and len(colour) == 7:
        colour = tuple(int(colour[i:i+2], 16) for i in range(1, 7, 2))
        self.colours[side] = colour

    # RGB colours
    elif ',' in colour:
        colour = colour.split(',')
        if len(colour) == 3:
            colour = tuple(int(value) for value in colour)
            if all(0 <= value < 256 for value in colour):
                self.colours[side] = colour
            else:
                raise ValueError

    # Named colours
    else:
        colours = {
            'white': (255,255,255),
            'black': (0,0,0),
            'red': (255,0,0),
            'orange': (255,165,0),
            'yellow': (255,255,0),
            'green': (0,128,0),
            'blue': (0,0,255),
            'purple': (128,0,128),
            'magenta': (255,0,255),
            'pink': (255,192,203),
            'cyan': (0,255,255),
            'brown': (165,42,42),
            'grey': (128,128,128),
            'gray': (128,128,128)
        }

        colour = colour.lower()
        if colour in colours:
            self.colours[side] = colours[colour]
        else:
            raise ValueError
