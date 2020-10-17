'''
Virtual Cube Program - Made by Fred Lang.
Simplify method.
'''

from cube.functions import split_move

#Simplify
def simplify(self, *move_types):
    moves = self.moves
    size = self.size

    all_move_types = ['CANCEL', 'PARALLEL', 'WIDE', 'SLICE', 'ROTATION']
    move_types = ' '.join(move_types).upper().split()

    if not move_types:
        move_types = ['ALL']

    if move_types == ['ALL']:
        move_types = all_move_types

    if not set(move_types).issubset(all_move_types):
        raise TypeError

    suffixes = "0123456789'"

    #Slice
    if 'SLICE' in move_types:
        num = 0
        while num < len(moves):
            depth, face, turns = split_move(moves[num], size)

            if depth[0] != 0 and depth[1] != size:
                moves[num] = face
                if depth[0] > 1:
                    moves[num] += 'w'
                if depth[0] > 2:
                    moves[num] = str(depth[0]) + moves[num]

                if turns % 4 == 1:
                    moves[num] += "'"
                elif turns % 4 == 2:
                    moves[num] += '2'

                moves.insert(num+1, face)

                if depth[1] > 1:
                    moves[num+1] += 'w'
                if depth[1] > 2:
                    moves[num+1] = str(depth[1]) + moves[num+1]

                if turns % 4 == 2:
                    moves[num+1] += '2'
                elif turns % 4 == 3:
                    moves[num+1] += "'"

                num += 1

            num += 1

    #Wide
    if 'WIDE' in move_types:
        num = 0
        while num < len(moves):
            depth, face, turns = split_move(moves[num], size)

            if depth[0] == 0 and size / 2 <= depth[1] < size:
                if depth[1] > size / 2 or face in 'LBD':
                    if face in 'UFR':
                        if face == 'U':
                            face = 'D'
                            rotation = 'y'
                        elif face == 'F':
                            face = 'B'
                            rotation = 'z'
                        else:
                            face = 'L'
                            rotation = 'x'

                        if turns % 4 == 2:
                            rotation += '2'
                        elif turns % 4 == 3:
                            rotation += "'"

                    else:
                        if face == 'L':
                            face = 'R'
                            rotation = 'x'
                        elif face == 'B':
                            face = 'F'
                            rotation = 'z'
                        else:
                            face = 'U'
                            rotation = 'y'

                        if turns % 4 == 1:
                            rotation += "'"
                        elif turns % 4 == 2:
                            rotation += '2'

                    depth[1] = size - depth[1]
                    moves[num] = face

                    if depth[1] > 1:
                        moves[num] += 'w'

                    if depth[1] > 2:
                        moves[num] = str(depth) + moves[num]

                    if turns % 4 == 2:
                        moves[num] += '2'
                    elif turns % 4 == 3:
                        moves[num] += "'"

                    moves.insert(num+1, rotation)
                    num += 1

            num += 1

    #Rotation
    if 'ROTATION' in move_types:
        rotations = []
        num = len(moves) - 1
        while num >= 0:
            depth, face, turns = split_move(moves[num], size)

            if depth[0] == 0 and depth[1] >= size:
                for turn in range(turns % 4):
                    last = ' '.join(moves[num+1:])

                    if face == 'U':
                        last = last.replace('L', ',').replace('l', '.')
                        last = last.replace('B', 'L').replace('b', 'l')
                        last = last.replace('R', 'B').replace('r', 'b')
                        last = last.replace('F', 'R').replace('f', 'r')
                        last = last.replace(',', 'F').replace('.', 'f')
                        last = last.replace('S', ',').replace('s', '.')
                        last = last.replace("M'", 'S').replace("m'", 's')
                        last = last.replace('M', "S'").replace('m', "s'")
                        last = last.replace(',', 'M').replace('.', 'm')

                    elif face == 'L':
                        last = last.replace('U', ',').replace('u', '.')
                        last = last.replace('F', 'U').replace('f', 'u')
                        last = last.replace('D', 'F').replace('d', 'f')
                        last = last.replace('B', 'D').replace('b', 'd')
                        last = last.replace(',', 'B').replace('.', 'b')
                        last = last.replace('S', ',').replace('s', '.')
                        last = last.replace("E'", 'S').replace("e'", 's')
                        last = last.replace('E', "S'").replace('e', "s'")
                        last = last.replace(',', 'E').replace('.', 'e')


                    elif face == 'F':
                        last = last.replace('U', ',').replace('u', '.')
                        last = last.replace('R', 'U').replace('r', 'u')
                        last = last.replace('D', 'R').replace('d', 'r')
                        last = last.replace('L', 'D').replace('l', 'd')
                        last = last.replace(',', 'L').replace('.', 'l')
                        last = last.replace('E', ',').replace('e', '.')
                        last = last.replace("M'", 'E').replace("m'", 'e')
                        last = last.replace('M', "E'").replace('m', "e'")
                        last = last.replace(',', 'M').replace('.', 'm')

                    elif face == 'R':
                        last = last.replace('U', ',').replace('u', '.')
                        last = last.replace('B', 'U').replace('b', 'u')
                        last = last.replace('D', 'B').replace('d', 'b')
                        last = last.replace('F', 'D').replace('f', 'd')
                        last = last.replace(',', 'F').replace('.', 'f')
                        last = last.replace('E', ',').replace('e', '.')
                        last = last.replace("S'", 'E').replace("s'", 'e')
                        last = last.replace('S', "E'").replace('s', "e'")
                        last = last.replace(',', 'S').replace('.', 's')

                    elif face == 'B':
                        last = last.replace('U', ',').replace('u', '.')
                        last = last.replace('L', 'U').replace('l', 'u')
                        last = last.replace('D', 'L').replace('d', 'l')
                        last = last.replace('R', 'D').replace('r', 'd')
                        last = last.replace(',', 'R').replace('.', 'r')
                        last = last.replace('M', ',').replace('m', '.')
                        last = last.replace("E'", 'M').replace("e'", 'm')
                        last = last.replace('E', "M'").replace('e', "m'")
                        last = last.replace(',', 'E').replace('.', 'e')

                    else:
                        last = last.replace('L', ',').replace('l', '.')
                        last = last.replace('F', 'L').replace('f', 'l')
                        last = last.replace('R', 'F').replace('r', 'f')
                        last = last.replace('B', 'R').replace('b', 'r')
                        last = last.replace(',', 'B').replace('.', 'b')
                        last = last.replace('M', ',').replace('m', '.')
                        last = last.replace("S'", 'M').replace("s'", 'm')
                        last = last.replace('S', "M'").replace('s', "m'")
                        last = last.replace(',', 'S').replace('.', 's')

                    moves[num+1:] = last.split()

                rotations.insert(0, moves[num])
                moves.pop(num)

            num -= 1

        moves.extend(self.reverse(self.orient()))

    #Parallel
    if 'PARALLEL' in move_types:
        num = 1
        while num < len(moves):
            depth, face, turns = split_move(moves[num], size)

            if face in 'LBD':
                depth = [size - depth[1], size - depth[0]]

                if face == 'L':
                    face = 'R'
                elif face == 'B':
                    face = 'F'
                else:
                    face = 'U'

            for i in range(num-1, -1, -1):
                last_depth, last_face, last_turns = split_move(moves[i], size)
                if last_face in 'LBD':
                    last_depth = [size - last_depth[1], size - last_depth[0]]

                    if last_face == 'L':
                        last_face = 'R'
                    elif last_face == 'B':
                        last_face = 'F'
                    else:
                        last_face = 'U'

                if face != last_face:
                    num += 1
                    break

                if depth != last_depth:
                    continue

                moves[i] = moves[i].rstrip(suffixes)
                turn = (last_turns + turns) % 4

                if turn == 1:
                    moves[i] += ''
                elif turn == 2:
                    moves[i] += '2'
                elif turn == 3:
                    moves[i] += "'"
                else:
                    moves.pop(num)
                    moves.pop(i)
                    num = i
                    break

                moves.pop(num)
                num = i + 1
                break
            else:
                num += 1

    #Cancel
    if 'CANCEL' in move_types:
        num = 1
        while num < len(moves):
            depth, face, turns = split_move(moves[num], size)
            last_depth, last_face, last_turns = split_move(moves[num-1], size)

            if depth == last_depth and face == last_face:
                moves[num-1] = moves[num-1].rstrip(suffixes)
                turns = (turns + last_turns) % 4

                if turns == 1:
                    moves[num-1] += ''
                elif turns == 2:
                    moves[num-1] += '2'
                elif turns == 3:
                    moves[num-1] += "'"
                else:
                    moves.pop(num)
                    moves.pop(num-1)
                    if num > 1:
                        num -= 1
                    continue

                moves.pop(num)
                continue

            num += 1

    return moves
