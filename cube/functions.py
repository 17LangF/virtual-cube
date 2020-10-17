'''
Virtual Cube Program - Made by Fred Lang.
Functions.
'''

#Issolved
def issolved(cube):
    return all(all(x == s[0][0] for y in s for x in y) for s in cube)

#Split move
def split_move(move, size):
    if not move:
        return False

    #Calculate depth of turn

    #Rotations
    elif move[0] in 'xyz':
        depth = [0, size]
        if move[0] == 'x':
            move = 'R'+move[1:]
        elif move[0] == 'y':
            move = 'U'+move[1:]
        else:
            move = 'F'+move[1:]

    #Slice moves
    elif move[0] in 'MmSsEe':
        if move[0].isupper():
            depth = [size//2, int(size/2+0.5)]
        else:
            depth = [1, size-1]

        if move[0] in 'Mm':
            move = 'L'+move[1:]
        elif move[0] in 'Ee':
            move = 'D'+move[1:]
        else:
            move = 'F'+move[1:]

    #Other moves
    elif move[0].isdigit():
        for i in range(len(move)):
            if not move[i].isdigit():
                break
        else:
            i += 1

        depth = [0, int(move[:i])]
        move = move[i:]

        if not move:
            return False

        if len(move) == 1:
            #e.g. 2U
            if move[0].isupper():
                depth[0] = depth[1]-1
            #e.g. 2u
            else:
                move = move.capitalize()

        else:
            if move[0] == '-':
                depth[0] = depth[1] - 1
                move = move[1:]

                if not move[0].isdigit():
                    return False

                for i in range(len(move)):
                    if not move[i].isdigit():
                        break
                else:
                    i += 1

                depth[1] = int(move[:i])
                move = move[i:]

                if not move:
                    return False

                #e.g. 2-3Uw
                if move[0].isupper():
                    if move[1:2] == 'w':
                        move = move[0] + move[2:]
                    else:
                        return False
                #e.g. 2-3u
                else:
                    move = move.capitalize()

            elif move[0].isupper():
                #e.g. 2Uw
                if move[1] == 'w':
                    move = move[0] + move[2:]
                #e.g. 2U'
                else:
                    depth[0] = depth[1]-1
            #e.g. 2u'
            else:
                move = move.capitalize()

    #e.g. u
    elif move[0].islower():
        depth = [0, 2]
        move = move.capitalize()

    else:
        if len(move) > 1:
            #e.g. Uw
            if move[1] == 'w':
                depth = [0, 2]
                move = move[0] + move[2:]
            #e.g. U'
            else:
                depth = [0, 1]
        #e.g. U
        else:
            depth = [0, 1]

    for i in range(2):
        if depth[i] > size:
            depth[i] = size
        elif depth[i] < 0:
            depth[i] = 0

    #Calculate number of 90 degree turns
    if len(move) > 1:
        #e.g. U2
        if move[1:].isnumeric():
            turns = int(move[1:])
        #e.g. U'
        elif len(move) == 2 and move[1] == "'":
            turns = -1
        #e.g. U2'
        elif move[1:-1].isnumeric() and move[-1] == "'":
            turns = -int(move[1:-1])
        else:
            return False
    #e.g. U
    else:
        turns = 1

    face = move[0]
    if face not in 'ULFRBD':
        return False

    return depth, face, turns

#Second to Days:Hours:Minutes:Seconds.Milliseconds
def convert_seconds(seconds):
    mS = int((seconds) * 1000)
    D, mS = divmod(mS, 86400000)
    H, mS = divmod(mS, 3600000)
    M, mS = divmod(mS, 60000)
    S, mS = divmod(mS, 1000)

    H = str(H).zfill(2)
    M = str(M).zfill(2)
    S = str(S).zfill(2)
    mS = str(mS).zfill(3)

    solve_time = f'{D}:{H}:{M}:{S}.{mS}'.lstrip('0:')

    if solve_time[0] == '.':
        solve_time = '0' + solve_time

    return solve_time

#Help
def help(function):
    if function == '':
        function = 'GENERAL'
    else:
        function = function.upper()

    with open('docs/help.txt', encoding='utf8') as f:
        lines = f.read().split('\n')

    should_print = False

    for line in lines:
        if line:
            if line.split()[0] == f'</{function}>':
                break
            if line.split()[0] == f'<{function}>':
                should_print = True
                continue
        if should_print:
            print(line)
    else:
        print(f'No help page for {function}.')

    #SHOW examples
    if function == 'SHOW':
        from cube import Cube
        cube = Cube()

        examples = (
            ('Change mode to 2D.', '2D'),
            ('Default SHOW function.', ''),
            ('Letters in colour.', 'letters'),
            ('Letters with background of colour.', 'letters bg,colour'),
            ('Letters with no colour.', 'letters 0'),
            ('Letters in black, underlined, with background of colour.',
             'letters fg,0,0,0,4,bg,colour'),
            ('Change letters to O.', 'O'),
            ('Blocks with foreground of colour and with no spaces.',
             'block fg,colour False'),
            ('Show last style again.', '')
        )

        print('\nSHOW 2D Examples:')

        for description, parameters in examples:
            print()
            print(description)
            print('SHOW',  parameters)
            print()
            cube.show(*parameters.split())

    #INPUT examples
    elif function == 'INPUT':
        from cube import Cube
        cube = Cube()

        examples = (
            ('SOLVED.',
             'UUUUUUUUULLLLLLLLLFFFFFFFFFRRRRRRRRRBBBBBBBBBDDDDDDDDD'),
            ('Checker board pattern.',
             'UDUDUDUDULRLRLRLRLFBFBFBFBFRLRLRLRLRBFBFBFBFBDUDUDUDUD'),
            ('Six spot pattern.',
             'UUUUFUUUULLLLDLLLLFFFFRFFFFRRRRURRRRBBBBLBBBBDDDDBDDDD'),
            ('Superflip pattern.',
             'UBULURUFULULBLFLDLFUFLFRFDFRURFRBRDRBUBRBLBDBDFDLDRDBD'),
            ('Cube in a cube in a cube pattern.',
             'UUUUFFUFRLLLDDLBDLFRUFRRFFFFURUURRRRBBBBLLBLDDDDBBDLBD')
        )

        print('\nExamples:')

        for description, parameters in examples:
            print()
            print(description)
            print('INPUT',  parameters)
            print()
            if description == 'SOLVED.':
                cube.show('2D')
                continue
            cube.input(parameters)
            cube.show()
