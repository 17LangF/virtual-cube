'''
Virtual Cube Program - Made by Fred Lang.
Main program.
'''

print('Importing...')

#Imports
try:
    import os

    from cube import Cube
    from cube.functions import convert_seconds, parse_moves
    from cube.help import help
    from cube.save import load, save

except ModuleNotFoundError as e:
    print(str(e).split()[-1] + ' could not be imported.')
    exit()

except AttributeError as e:
    print("'" + str(e).split("'")[-2] + ".py' was not found.")
    exit()

#Freeplay
def freeplay():
    screen_size = 79
    os.system('cls')

    print('''
Virtual Cube Program - Made by Fred Lang.
Enter HELP for list of functions.\
''')

    cube = Cube()
    functions = [i for i in dir(cube) if callable(getattr(cube, i))
                 and not i.startswith('_') and i not in ('MoveError', 'move')]

    print()
    cube.show()
    print()

    while True:
        print('='*screen_size)
        print()
        moves = input('Enter move(s) or function: ').strip()
        print()

        if not moves:
            continue

        function = moves.split()[0].upper()
        if len(moves.split()) > 1:
            args = moves.split(maxsplit=1)[1]
        else:
            args = ''

        #Exit
        if function == 'EXIT':
            raise SystemExit

        #Help
        elif function == 'HELP':
            try:
                if args:
                    help(args.upper())
                else:
                    help()
            except FileNotFoundError as e:
                print(str(e).split(': ')[1], 'was not found.')

        #Load
        elif function == 'LOAD':
            if args:
                filename = f'saves/{args}.txt'
            else:
                filename = 'saves/Cube.txt'

            try:
                cube = load(filename)
            except FileNotFoundError as e:
                print(str(e).split(': ')[1], 'was not found.\n')
                continue
            except:
                print('Failed to load.\n')
                continue

            print(f"Successfully loaded '{filename}'.\n")

            for name, moves in ('SCRAMBLE',cube.smoves), ('MOVES',cube.moves):
                if moves:
                    print(f'{name}: {" ".join(moves)}\n')
                else:
                    print(f'{name}: No moves\n')

            cube.show()

        #Save
        elif function == 'SAVE':
            if args:
                filename = f'saves/{args}.txt'
            else:
                filename = 'saves/Cube.txt'

            try:
                save(cube, filename)
            except FileNotFoundError:
                print('Could not create file.\n')
                continue

            print(f"Successfully saved in '{filename}'.")

        #Functions
        elif function.lower() in functions:
            if (function in ('PLAY', 'REPEAT') or function == 'SCRAMBLE' and
                args[:5].upper() not in ('MOVES', 'STATE')):
                try:
                    args = parse_moves(args)
                except Cube.MoveError as e:
                    print(f'{e}\n')
                    continue
            else:
                args = args.split()

            try:
                result = getattr(cube, function.lower())(*args)
            except Cube.MoveError as e:
                print(f'{e}\n')
                continue
            except TypeError:
                print('Incorrect arguments given.\n')
                continue
            except FileNotFoundError as e:
                print(str(e).split(': ')[1], 'was not found.\n')
                continue

            if function in ('COLOUR', 'INPUT', 'INVERT', 'MIRROR', 'UNDO'):
                cube.show()

            elif function == 'LINK':
                if result:
                    print(result)
                else:
                    print('Size is not supported by alg.cubing.net.')

            elif function == 'MOVECOUNT':
                for metric in result:
                    print(f'{metric}: {result[metric]}')

            elif function == 'REPEAT':
                if not result:
                    print(f'Did not solve.\n')
                elif result == 1:
                    print(f'1 repetition.\n')
                else:
                    print(f'{result} repetitions.\n')
                cube.show()

            elif function == 'RESET':
                os.system('cls')
                print()
                cube.show()

            elif function == 'SCRAMBLE':
                if result:
                    print(f'SCRAMBLE: {" ".join(result)}')
                    cube.reset(cube.size)
                    print()
                    cube.show()
                    cube.play(*result)
                    cube.smoves = result
                    cube.moves = []
                elif result == []:
                    print('SCRAMBLE: No moves')

            elif function == 'SIMPLIFY':
                if result:
                    print(' '.join(result))
                else:
                    print('No moves.')

            elif function == 'SOLVE':
                solve, stats, solve_time = result
                if solve == False:
                    print('Could not solve.')

                elif isinstance(solve, int):
                    cube.show()
                    print(f'SOLVED: {solve}\n')

                    table = [['', *stats['AVERAGE'].keys()]]
                    for stat in stats:
                        table.append([stat, *stats[stat].values()])

                    def length(var):
                        if isinstance(var, int):
                            return len(str(var))
                        elif isinstance(var, float):
                            return len(f'{var:.6f}')
                        else:
                            return len(var)

                    columns = [max(map(length, column)) for column in table]
                    table = [list(row) for row in zip(*table)]

                    for row in table:
                        for x, value in enumerate(row):
                            if isinstance(value, int):
                                row[x] = f'{row[x]:{columns[x]}}'
                            elif isinstance(value, float):
                                row[x] = f'{row[x]:{columns[x]}.6f}'
                            else:
                                row[x] = f'{row[x]:^{columns[x]}}'

                    line = ['', *('-' * column for column in columns), '']
                    line = '+'.join(line)

                    for row in table:
                        if (row[0].strip() in ('', 'TIME') or
                            len(table) > 7 and row[0].strip() == 'HTM'):
                            print(line)
                        print('|'.join(('', *row, '')))
                        if row[0].strip() in ('', 'TIME'):
                            print(line)

                    print(f'\nTOTAL TIME: {convert_seconds(solve_time)}')

                else:
                    if solve:
                        print(f'SOLUTION: {" ".join(solve)}')
                        cube.undo(len(solve))
                        cube.play(*solve)
                    else:
                        print('SOLUTION: No moves')

                    if len(stats) > 5:
                        print()

                    for stat in stats:
                        if stat in ('HTM', 'TIME'):
                            print()
                        if stats[stat] == '':
                            print(f'{stat}: None')
                        elif stat == 'TIME':
                            print(f'{stat}: {stats[stat]:.6f}')
                        else:
                            print(f'{stat}: {stats[stat]}')

            elif function == 'SPEEDSOLVE':
                os.system('cls')
                print()
                cube.show()
                print()

                if not result['TIME'][0] == 'D':
                    print('Solved!')

                print(f'TIME: {result["TIME"]}')
                print('\nMOVECOUNT:')
                for stat in 'HTM', 'QTM', 'STM', 'ETM':
                    print(f'{stat}: {result[stat]}')

                print()

                for stat in 'TPS', 'START TIME', 'END TIME':
                    print(f'{stat}: {result[stat]}')

        #Attributes
        elif function == 'CUBE':
            print(''.join(x for s in cube.cube for y in s for x in y))

        elif function == 'SIZE':
            print(cube.size)

        elif function == 'MOVES':
            if len(cube.moves) == 0:
                print('No moves.')
            else:
                print(' '.join(cube.moves))

        elif function == 'SMOVES':
            if len(cube.smoves) == 0:
                print('No moves.')
            else:
                print(' '.join(cube.smoves))

        elif function == 'SHOWSTYLE':
            for info in cube.showstyle:
                print(f'{info}: {cube.showstyle[info]}')

        elif function == 'COLOURS':
            for side, (r,g,b) in cube.colours.items():
                print(f'{side}: #{r:02x}{g:02x}{b:02x} or {r}, {g}, {b}')

        #Moves
        else:
            try:
                moves = parse_moves(moves)
                cube.move(moves)
            except Cube.MoveError as e:
                print(f'{e}\n')
                continue

            cube.show()

        print()

if __name__ == '__main__':
    try:
        freeplay()
    except (EOFError, KeyboardInterrupt):
        exit()
