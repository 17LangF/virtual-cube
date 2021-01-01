'''
Virtual Cube Program - Made by Fred Lang.
Functions.
'''

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

#Issolved
def issolved(cube):
    return all(all(x == s[0][0] for y in s for x in y) for s in cube)

#Orient
def orient(cube):
    size = len(cube[0])

    if size % 2:
        mid = size // 2
        centres = [side[mid][mid] for side in cube]

        if {'U','F'}.issubset(centres):
            u = centres.index('U')
            f = centres.index('F')
        else:
            return False

    else:
        vertices = (
            ((0,0,0),(4,0,-1),(1,0,0)),
            ((0,0,-1),(3,0,-1),(4,0,0)),
            ((0,-1,-1),(2,0,-1),(3,0,0)),
            ((0,-1,0),(1,0,-1),(2,0,0)),
            ((5,0,0),(2,-1,0),(1,-1,-1)),
            ((5,0,-1),(3,-1,0),(2,-1,-1)),
            ((5,-1,-1),(4,-1,0),(3,-1,-1)),
            ((5,-1,0),(1,-1,0),(4,-1,-1))
        )

        for v in vertices:
            vertex = [cube[v[i][0]][v[i][1]][v[i][2]] for i in range(3)]

            if set(vertex) == set('DBL'):
                u = v[vertex.index('D')][0]
                f = v[vertex.index('B')][0]

                if u == 0:
                    u = 5
                elif u == 5:
                    u = 0
                else:
                    u = (u + 1) % 4 + 1

                if f == 0:
                    f = 5
                elif f == 5:
                    f = 0
                else:
                    f = (f + 1) % 4 + 1

    orientations = (
        (False, ["y'"], [], ['y'], ['y2'], False),
        (['z','y'], False, ['z'], False, ['z','y2'], ['z',"y'"]),
        (['x','y2'], ['x',"y'"], False, ['x','y'], False, ['x']),
        (["z'","y'"], False, ["z'"], False, ["z'",'y2'], ["z'",'y']),
        (["x'"], ["x'","y'"], False, ["x'",'y'], False, ["x'",'y2']),
        (False, ['x2',"y'"], ['z2'], ['x2','y'], ['x2'], False)
    )

    return orientations[u][f]

#Parse moves
def parse_moves(moves):
    from cube import Cube

    #Split joined moves
    i = 0
    previous_move = False
    while i < len(moves):
        if moves[i] in ' ()[],:':
            previous_move = False
        elif moves[i].upper() in 'ULFRBDMESXYZ':
            if previous_move:
                moves = f'{moves[:i]} {moves[i:]}'
                i += 2
                continue
            else:
                previous_move = True
        i += 1

    #Bracketed moves
    while any(bracket in moves for bracket in '()[]'):
        brackets = []
        for i, char in enumerate(moves):
            if char in '([':
                brackets.append((char, i))

            elif char in ')]':
                if (len(brackets) == 0 or
                    brackets[-1][0] != '(['[')]'.index(char)]):
                    raise Cube.MoveError('Brackets are not balanced.')

                bracket = moves[brackets[-1][1]+1: i]

                if char == ']':
                    for separator in ',:':
                        if bracket.count(separator) == 1:
                            a,b = bracket.split(separator)
                            a = a.strip()
                            b = b.strip()
                            if not (a and b):
                                raise Cube.MoveError(
                                    'There must be at least one move on both '
                                    'sides of the separator.')
                            break
                    else:
                        raise Cube.MoveError(
                            'Square brackets must contain one comma or one '
                            'colon.')

                    #Commutator
                    if separator == ',':
                        reverse_a = ' '.join(reverse(a.split()))
                        reverse_b = ' '.join(reverse(b.split()))
                        bracket = f'{a} {b} {reverse_a} {reverse_b}'

                    #Conjugate
                    else:
                        reverse_a = ' '.join(reverse(a.split()))
                        bracket = f'{a} {b} {reverse_a}'

                #Repetition
                if i < len(moves) - 1:
                    for end, char in enumerate(moves[i+1:], i+1):
                        if not char.isdigit():
                            break
                    else:
                        end += 1

                    if end > i + 1:
                        bracket = ' '.join([bracket] * int(moves[i + 1: end]))

                    if end < len(moves):
                        if char == "'":
                            bracket = ' '.join(reverse(bracket.split()))
                            end += 1
                else:
                    end = len(moves)

                moves = moves[:brackets[-1][1]], bracket, moves[end:]
                moves = ' '.join(moves).strip()
                break

        else:
            if len(brackets) != 0:
                raise Cube.MoveError('Brackets are not balanced.')

    return moves.split()

#Reverse
def reverse(moves):
    reverse = []
    for move in moves[::-1]:
        if move[-1] == "'":
            reverse.append(move[:-1])
        elif move[-1] == '2':
            reverse.append(move)
        else:
            reverse.append(move + "'")

    return reverse

#Split move
def split_move(move, size):
    from cube import Cube

    start_move = move
    #Calculate depth of turn

    #Rotations
    if move[0] in 'xyz':
        depth = [0, size]
        if move[0] == 'x':
            move = 'R'+move[1:]
        elif move[0] == 'y':
            move = 'U'+move[1:]
        else:
            move = 'F'+move[1:]

    #Slice moves
    elif move[0] in 'MmEeSs':
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
        for i, char in enumerate(move):
            if not char.isdigit():
                break
        else:
            i += 1

        depth = [0, int(move[:i])]
        move = move[i:]

        if not move:
            raise Cube.MoveError(f'"{start_move}" is invalid.')

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
                    raise Cube.MoveError(f'"{start_move}" is invalid.')

                for i, char in enumerate(move):
                    if not char.isdigit():
                        break
                else:
                    i += 1

                depth[1] = int(move[:i])
                move = move[i:]

                if not move:
                    raise Cube.MoveError(f'"{start_move}" is invalid.')

                #e.g. 2-3Uw
                if move[0].isupper():
                    if move[1:2] == 'w':
                        move = move[0] + move[2:]
                    else:
                        raise Cube.MoveError(f'"{start_move}" is invalid.')
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
            raise Cube.MoveError(f'"{start_move}" is invalid.')
    #e.g. U
    else:
        turns = 1

    face = move[0]
    if face not in 'ULFRBD':
        raise Cube.MoveError(f'"{start_move}" is invalid.')

    return depth, face, turns
