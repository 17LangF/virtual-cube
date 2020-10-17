'''
Virtual Cube Program - Made by Fred Lang.
Main program.
'''

try:
    import os

    from cube import Cube
    from cube.functions import help
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
    cube = Cube()

    print()
    cube.show()
    print()

    while True:
        print('='*screen_size)
        print()
        move = input('Enter move(s) or function: ').strip()
        print()
        if not move:
            continue

        function = move.split()[0].upper()
        if len(move.split()) > 1:
            args = move.split(maxsplit=1)[1]
        else:
            args = ''

        #Help
        if function == 'HELP':
            try:
                help(args)
            except FileNotFoundError as e:
                print(str(e).split(': ')[1], 'was not found.')

        #Functions
        elif function in cube.functions:
            args = args.split()
            try:
                result = cube.functions[function](*args)
            except TypeError:
                print('Incorrect arguments given.\n')
                continue
            except FileNotFoundError as e:
                print(str(e).split(': ')[1], 'was not found.')

            if function in ('SCRAMBLE', 'COMMUTATOR', 'CONJUGATE', 'REVERSE',
                            'SIMPLIFY'):
                if result:
                    print(' '.join(result))
                else:
                    print('No moves.')

            if function in ('SCRAMBLE', 'COMMUTATOR', 'CONJUGATE'):
                print()

            if function in ('RESET', 'SCRAMBLE', 'MOVE', 'UNDO', 'COMMUTATOR',
                            'CONJUGATE', 'INVERT', 'INPUT'):
                cube.show()

            if function == 'REPEAT':
                if result == 1:
                    print(f'1 repetition.\n')
                else:
                    print(f'{result} repetitions.\n')
                cube.show()

            if function == 'ORIENT':
                if result is False:
                    print(result)
                    print('Cannot orient.')
                elif result:
                    print(' '.join(result))
                else:
                    print('No moves')

            if function == 'LINK':
                if result:
                    print(result)
                else:
                    print('Size is not supported by alg.cubing.net.')

            if function == 'MOVECOUNT':
                for metric in result:
                    print(f'{metric}: {result[metric]}')

            if function == 'SPEEDSOLVE':
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

            if function == 'SOLVE':
                solve, stats, solve_time = result
                if solve is False:
                    print('Could not solve.\n')
                    continue

                if solve:
                    print(f'SOLUTION: {" ".join(solve)}\n')
                else:
                    print('SOLUTION: No moves\n')

                old = cube.movecount()

                for num in range(len(solve)):
                    cube.show()
                    choice = input().strip().upper()

                    if choice:
                        if choice == 'EXIT':
                            for move in solve[num:]:
                                cube.move(move)
                            break

                        if choice.split()[0] == 'PLAY':
                            cube.play(solve[num:], *choice.split()[1:])
                            break

                    cube.move(solve[num])
                    print(solve[num])
                    print()

                os.system('cls')
                print()
                cube.show()

                print()
                for stat in stats:
                    print(f'{stat}: {stats[stat]}')

                if stats:
                    print()

                print(f'TIME: {solve_time:.6f}')

                new = cube.movecount()

                print('\nMOVECOUNT:')
                for stat in new:
                    print(f'{stat}: {new[stat] - old[stat]}')

        #Attributes
        elif function == 'CUBE':
            print(cube.cube)

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
            for i in cube.showstyle:
                print(f'{i}: {cube.showstyle[i]}')

        elif function == 'COLOURS':
            for i in cube.colours:
                print(f'{i}: {cube.colours[i]}')

        #Moves
        else:
            should_print = False
            for move in move.split():
                if cube.move(move):
                    should_print = True
                else:
                    print(f'{move} is invalid.')

            if should_print:
                cube.show()

        print()

if __name__ == '__main__':
    print('''
Virtual Cube Program - Made by Fred Lang.
Enter HELP for list of functions.\
''')
    try:
        freeplay()
    except KeyboardInterrupt:
        exit()
    except ArithmeticError:
        print('An unknown error occured.')
        exit()
