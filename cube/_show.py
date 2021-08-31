"""Show cube."""

import importlib
import turtle
from math import sin, cos, radians


def show(self, *show_style):
    """
    Show cube.

    Parameters
    ----------
    *show_style : str
        Can be '3D' or '2D' to change the dimension used to show the
        cube or be arguments passed into `show3D` or `show2D` to change
        the style used to show the cube.
    """
    if ' '.join(show_style).upper() == '2D':
        self.show_style['DIMENSION'] = 2
        show_style = []
    elif ' '.join(show_style).upper() == '3D':
        self.show_style['DIMENSION'] = 3
        show_style = []

    if self.show_style['DIMENSION'] == 2:
        self.show2D(*show_style)
    else:
        self.show3D(*show_style)


def show3D(self, *show_style):
    """
    Use Python Turtle to display a 3D drawing of the cube.

    Parameters
    ----------
    *show_style : str or float
        Up to 5 positional arguments can be passed: `xr`, `yr`, `zc`,
        `zoom`, `pensize`. If an argument is not given, the last used
        value is used. They must all be values that can be converted to
        floats.

        xr : str or float
            The angle of rotation about the x axis in degrees.
            -38 <= `xr` <= 38.
        yr : str or float
            The angle of rotation about the y axis in degrees.
            -45 <= `yr` <= 45.
        zc : str or float
            The size difference between close and far points.
        zoom : str or float
            How much larger the picture is drawn. Negative inverts
            drawing.
        pensize : str or float
            Thickness of the black lines. Default is
            abs(zoom) / (5 * size + 5).
    """
    cube = self.cube
    size = self.size
    colours = self.colours

    # Get info
    if len(show_style) > 5:
        raise TypeError

    show_style = list(map(float, show_style))
    self.show_style['3D'][:len(show_style)] = show_style
    xr, yr, zc, zoom, pensize = self.show_style['3D']

    if len(show_style) == 4:
        self.show_style['3D'][4] = abs(zoom) / (5 * size + 5)
        pensize = self.show_style['3D'][4]
    if pensize < 0:
        self.show_style['3D'][4] = 0
        pensize = 0

    sides = []
    if xr > 0:
        sides.append(0)
    else:
        sides.append(5)

    if yr > 0:
        sides.append(3)
    else:
        sides.append(1)

    if abs(xr) > abs(yr):
        sides = sides[::-1]

    sides.append(2)

    if abs(xr) > 38:
        xr = ((xr > 0) * 2 - 1) * 38
        self.show_style['3D'][0] = xr
    if abs(yr) > 45:
        yr = ((yr > 0) * 2 - 1) * 45
        self.show_style['3D'][1] = yr

    if zc:
        zc = 1 / zc
    xr, yr = radians(xr), radians(yr)

    # Reset screen
    try:
        turtle.isvisible()
    except turtle.Terminator:
        importlib.reload(turtle)

    if turtle.isvisible():
        turtle.title("Virtual Cube - Made by Fred Lang")
        turtle.setup(width=0.5, height=1.0, startx=-1)
        turtle.colormode(255)
        turtle.hideturtle()
        turtle.tracer(0, 0)
        turtle.penup()

    turtle.clear()
    turtle.pensize(pensize)

    if not size:
        turtle.goto(0, 0)
        turtle.dot()
        turtle.update()
        return

    # Get co-ordinates
    coords = {s: [[0]*(size+1) for _ in range(size+1)] for s in sides}

    for s in sides:
        for y_coord in range(size + 1):
            for x_coord in range(size + 1):
                x = x_coord / size * 2 - 1
                y = y_coord / size * 2 - 1

                if not s:
                    x, y, z = x, 1, -y
                elif s == 1:
                    x, y, z = -1, -y, -x
                elif s == 2:
                    x, y, z = x, -y, -1
                elif s == 3:
                    x, y, z = 1, -y, x
                elif s == 4:
                    x, y, z = -x, -y, 1
                else:
                    x, y, z = x, -1, y

                # Rotate about the y axis
                x, z = x * cos(yr) + z * sin(yr), z * cos(yr) - x * sin(yr)
                # Rotate about the x axis
                y, z = y * cos(xr) + z * sin(xr), z * cos(xr) - y * sin(xr)

                if zc:
                    x = x / (z + zc) * zc
                    y = y / (z + zc) * zc

                coords[s][y_coord][x_coord] = x * zoom, y * zoom

    # Draw cube
    for s in coords:
        for y in range(size):
            for x in range(size):
                turtle.goto(*coords[s][y][x])
                turtle.pendown()
                turtle.fillcolor(colours[cube[s][y][x]])
                turtle.begin_fill()
                turtle.goto(*coords[s][y+1][x])
                turtle.goto(*coords[s][y+1][x+1])
                turtle.goto(*coords[s][y][x+1])
                turtle.goto(*coords[s][y][x])
                turtle.end_fill()
                turtle.penup()

    turtle.update()
    turtle.onscreenclick(lambda x, y: self.show3D(str(-y/4), str(-x/4)))


def show2D(self, *show_style: str):
    """
    Print cube in the terminal as a 2D net.

    Parameters
    ----------
    *show_style : str
        Up to 3 positional arguments can be passed: `sticker`,
        `colour_code`, `spaces`. If an argument is not given, the last
        used value is used.

        sticker : str, optional
            Character(s) used to represent one sticker.

            If `sticker` == 'letters', then each sticker will be shown
            with its corresponding letter.

            If `sticker` == 'block', two block characters
            '\u2588\u2588' will be used.
        colour_code : str, optional
            ANSI character escape codes.

            Colour codes:
                colour: Colour of sticker in R,G,B
                fg: Foreground colour (38,2) followed by colour in the
                form R,G,B.
                bg: Background colour (48,2) followed by colour in the
                form R,G,B.
                0: No colour
                4: Underline
            Colour codes are separated with commas.
        spaces : {'True', 'False'}, optional
            Whether or not the faces should be separated.

    Notes
    -----
    Uses ANSI escape codes to show colours in the terminal. For more
    information, see https://en.wikipedia.org/wiki/ANSI_escape_code.
    """
    if len(show_style) > 3:
        raise TypeError

    # Retrieve last show_style and save given arguments
    cube = [[y[:] for y in s] for s in self.cube]
    size = self.size
    colours = self.colours
    colours = {s: ','.join(map(str, colours[s])) for s in colours}

    if show_style:
        self.show_style['2D'][0] = show_style[0]

    if len(show_style) > 1:
        self.show_style['2D'][1] = show_style[1]

    if len(show_style) > 2:
        if show_style[2].upper() == 'TRUE':
            self.show_style['2D'][2] = True
        elif show_style[2].upper() == 'FALSE':
            self.show_style['2D'][2] = False
        else:
            raise ValueError

    sticker, colour_codes, spaces = self.show_style['2D']

    # Format colours and stickers
    sticker = sticker.replace('block', '\u2588\u2588')
    colour_codes = colour_codes.replace('fg', '38,2').replace('bg', '48,2')
    letters = sticker == 'letters'

    for s in range(6):
        for y in range(size):
            for x in range(size):
                if letters:
                    sticker = cube[s][y][x]
                if cube[s][y][x] in colours:
                    colour = colours[cube[s][y][x]]
                else:
                    colour = colours['U']
                colour_code = colour_codes.replace('colour', colour)
                colour_code = ';'.join(colour_code.split(','))
                cube[s][y][x] = f'\x1B[{colour_code}m{sticker}\x1B[0m'

    # Join stickers together
    gap = spaces * '  '
    line = size * len(sticker) * ' '
    cube[0] = (f'\n  {line}{gap}{"".join(y)}' for y in cube[0])
    cube[1:5] = [list(zip(*cube[1:5]))]
    cube[1] = (f'\n  {gap.join("".join(s) for s in y)}' for y in cube[1])
    cube[2] = (f'\n  {line}{gap}{"".join(y)}' for y in cube[2])
    cube = (spaces*'\n').join(''.join(y) for y in cube)[1:]

    print(cube)
