'''
Virtual Cube Program - Made by Fred Lang.
Show method.
'''

import time
import turtle
from math import sin, cos, radians

#Show
def show(self, *show_style):
    if ' '.join(show_style).upper() == 'OFF':
        self.showstyle['SHOW'] = False

    elif ' '.join(show_style).upper() == 'ON':
        self.showstyle['SHOW'] = True
        show_style = []

    if not self.showstyle['SHOW']:
        return

    if ' '.join(show_style).upper() == '2D':
        self.showstyle['DIMENSION'] = 2
        show_style = []

    elif ' '.join(show_style).upper() == '3D':
        self.showstyle['DIMENSION'] = 3
        show_style = []

    if self.showstyle['DIMENSION'] == 3:
        self.show3D(*show_style)
        return

    if len(show_style) > 3:
        raise TypeError

    #Retrieve last show_style and save given arguments
    cube = [[y[:] for y in s] for s in self.cube]
    size = self.size
    colours = self.colours
    colours = {s: ','.join(map(str, colours[s])) for s in colours}

    if show_style:
        self.showstyle['STICKER'] = show_style[0]

    if len(show_style) > 1:
        self.showstyle['COLOUR_CODES'] = show_style[1]

    if len(show_style) > 2:
        if show_style[2].upper() == 'TRUE':
            self.showstyle['SPACES'] = True
        elif show_style[2].upper() == 'FALSE':
            self.showstyle['SPACES'] = False
        else:
            raise TypeError

    sticker = self.showstyle['STICKER']
    colour_codes = self.showstyle['COLOUR_CODES']
    spaces = self.showstyle['SPACES']

    #Format colours and stickers
    sticker = sticker.replace('block', '██')
    colour_codes = colour_codes.replace('fg', '38,2').replace('bg', '48,2')
    letters = sticker == 'letters'

    for a in range(6):
        for b in range(size):
            for c in range(size):
                if letters:
                    sticker = cube[a][b][c]
                if cube[a][b][c] in colours:
                    colour = colours[cube[a][b][c]]
                else:
                    colour = colours['U']
                colour_code = colour_codes.replace('colour', colour)
                colour_code = ';'.join(colour_code.split(','))
                cube[a][b][c] = f'\x1B[{colour_code}m{sticker}\x1B[0m'

    #Join stickers together
    gap = spaces * '  '
    line = size * len(sticker) * ' '

    cube[0] = (f'\n  {line}{gap}{"".join(y)}' for y in cube[0])
    cube[1:5] = [list(zip(*cube[1:5]))]
    cube[1] = (f'\n  {gap.join("".join(s) for s in y)}' for y in cube[1])
    cube[2] = (f'\n  {line}{gap}{"".join(y)}' for y in cube[2])

    cube = (spaces*'\n').join(''.join(y) for y in cube)[1:]

    print(cube)
    return cube

#Show 3D
def show3D(self, *info):
    cube = self.cube
    size = self.size
    colours = self.colours

    if len(info) > 5:
        raise TypeError

    #Reset screen
    try:
        turtle.isvisible()
    except turtle.Terminator:
        try:
            from importlib import reload
        except ImportError:
            print('Could not import importlib.')
            return

        reload(turtle)

    if turtle.isvisible():
        turtle.title('Virtual Cube - Made by Fred Lang')
        turtle.setup(width=0.5, height=1.0, startx=-1)
        turtle.colormode(255)
        turtle.hideturtle()
        turtle.tracer(0,0)
        turtle.penup()

    turtle.pensize(self.showstyle['3D INFO'][4])
    turtle.clear()

    if size == 0:
        turtle.goto(0,0)
        turtle.dot(10)
        turtle.update()
        return

    #Reset co-ordinates
    if info or len(self.showstyle['3D COORDS'][2]) != size + 1:
        for i in range(len(info)):
            try:
                self.showstyle['3D INFO'][i] = float(info[i])
            except ValueError:
                raise TypeError


        xr,yr,zc,zoom,pensize = self.showstyle['3D INFO']

        if len(info) < 5:
            self.showstyle['3D INFO'][4] = abs(zoom) / (5 * size + 10)

        sides = []

        if xr > zc * 40:
            sides.append(0)
            if xr > 45:
                xr = 45
        elif xr < -zc * 40:
            sides.append(5)
            if xr < -45:
                xr = -45

        if yr > zc * 40:
            sides.append(3)
            if yr > 45:
                yr = 45
        elif yr < -zc * 40:
            sides.append(1)
            if yr < -45:
                yr = -45

        sides.append(2)

        if zc:
            zc = 1 / zc
        xr,yr = radians(xr), radians(yr)

        coords = {s: [[0]*(size+1) for i in range(size+1)] for s in sides}

        for s in sides:
            for y_coord in range(size + 1):
                for x_coord in range(size + 1):
                    x = x_coord / size * 2 - 1
                    y = y_coord / size * 2 - 1

                    if s == 0:
                        x,y,z = x,1,-y
                    elif s == 1:
                        x,y,z = -1,-y,-x
                    elif s == 2:
                        x,y,z = x,-y,-1
                    elif s == 3:
                        x,y,z = 1,-y,x
                    elif s == 4:
                        x,y,z = -x,-y,1
                    else:
                        x,y,z = x,-1,y

                    x = x * cos(yr) + z * sin(yr)
                    z = z * cos(yr) - x * sin(yr)

                    y = y * cos(xr) + z * sin(xr)
                    z = z * cos(xr) - y * sin(xr)

                    if zc:
                        x = x / (z + zc) * zc
                        y = y / (z + zc) * zc

                    coords[s][y_coord][x_coord] = x * zoom, y * zoom

        self.showstyle['3D COORDS'] = coords

    else:
        coords = self.showstyle['3D COORDS']

    #Draw cube
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
    turtle.onscreenclick(lambda x,y: self.show(str(-y/4),str(-x/4)))
