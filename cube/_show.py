'''
Virtual Cube Program - Made by Fred Lang.
Show method.
'''

import turtle
from math import sin, cos, radians

#Show
def show(self, *showstyle):
    if ' '.join(showstyle).upper() == 'OFF':
        self.showstyle['SHOW'] = False

    elif ' '.join(showstyle).upper() == 'ON':
        self.showstyle['SHOW'] = True
        showstyle = []

    if not self.showstyle['SHOW']:
        return

    if ' '.join(showstyle).upper() == '2D':
        self.showstyle['DIMENSION'] = 2
        showstyle = []

    elif ' '.join(showstyle).upper() == '3D':
        self.showstyle['DIMENSION'] = 3
        showstyle = []

    if self.showstyle['DIMENSION'] == 2:
        self.show2D(*showstyle)
    else:
        self.show3D(*showstyle)

#Show 3D
def show3D(self, *showstyle):
    cube = self.cube
    size = self.size
    colours = self.colours

    if len(showstyle) > 5:
        raise TypeError

    #Get info
    for i, info in enumerate(showstyle):
        try:
            self.showstyle['3D'][i] = float(info)
        except ValueError:
            raise TypeError

    xr,yr,zc,zoom,pensize = self.showstyle['3D']

    if len(showstyle) == 4:
        self.showstyle['3D'][4] = abs(zoom) / (5 * size + 5)
        pensize = self.showstyle['3D'][4]

    if pensize < 0:
        self.showstyle['3D'][4] = 0
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
        self.showstyle['3D'][0] = xr
    if abs(yr) > 45:
        yr = ((yr > 0) * 2 - 1) * 45
        self.showstyle['3D'][1] = yr

    if zc:
        zc = 1 / zc
    xr,yr = radians(xr), radians(yr)

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

    turtle.clear()
    turtle.pensize(pensize)

    if size == 0:
        turtle.goto(0,0)
        turtle.dot()
        turtle.update()
        return

    #Get co-ordinates
    coords = {s: [[0]*(size+1) for _ in range(size+1)] for s in sides}

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

                #Rotate about the y axis
                x,z = x * cos(yr) + z * sin(yr), z * cos(yr) - x * sin(yr)

                #Rotate about the x axis
                y,z = y * cos(xr) + z * sin(xr), z * cos(xr) - y * sin(xr)

                if zc:
                    x = x / (z + zc) * zc
                    y = y / (z + zc) * zc

                coords[s][y_coord][x_coord] = x * zoom, y * zoom

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
    turtle.onscreenclick(lambda x,y: self.show3D(str(-y/4), str(-x/4)))

def show2D(self, *showstyle):
    if len(showstyle) > 3:
        raise TypeError

    #Retrieve last showstyle and save given arguments
    cube = [[y[:] for y in s] for s in self.cube]
    size = self.size
    colours = self.colours
    colours = {s: ','.join(map(str, colours[s])) for s in colours}

    if showstyle:
        self.showstyle['2D'][0] = showstyle[0]

    if len(showstyle) > 1:
        self.showstyle['2D'][1] = showstyle[1]

    if len(showstyle) > 2:
        if showstyle[2].upper() == 'TRUE':
            self.showstyle['2D'][2] = True
        elif showstyle[2].upper() == 'FALSE':
            self.showstyle['2D'][2] = False
        else:
            raise TypeError

    sticker, colour_codes, spaces = self.showstyle['2D']

    #Format colours and stickers
    sticker = sticker.replace('block', '██')
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
