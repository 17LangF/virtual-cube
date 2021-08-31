"""
Virtual Cube Program - Made by Fred Lang.

Allow the user to input functions with arguments and make moves to
control a Rubik's Cube.
"""

try:
    import os
    import statistics

    from cube import Cube, CubeError, MoveError
    from cube.functions import convert_seconds, parse_moves
    from cube.manual import manual
    from cube.save import load, save

except ModuleNotFoundError as e:
    print(str(e).split()[-1] + " could not be imported.")
    raise SystemExit

except AttributeError as e:
    print("'" + str(e).split("'")[-2] + ".py' was not found.")
    raise SystemExit


def freeplay():
    """
    Create a command line interface to control a Rubik's Cube.

    Cube functions:
        COLOUR: Change the colour of a side of the cube.
        EXIT: Exit program.
        HELP: Return help page for a given function.
        INPUT: Set the state of the cube.
        INVERT: Switch to the inverse scramble and reverse moves.
        LINK: Return an alg.cubing.net link for the cube.
        LOAD: Load a cube from a previously saved file.
        MIRROR: Mirror all moves across a plane.
        MOVECOUNT: Return current move count.
        PLAY: Play through moves one at a time.
        REPEAT: Repeat moves until solved.
        RESET: Reset cube and set cube size.
        SAVE: Save cube attributes to a file.
        SCRAMBLE: Reset and scramble cube.
        SHOW: Show cube.
        SIMPLIFY: Simplify moves.
        SOLVE: Compute a solution to solve the cube.
        SPEEDSOLVE: Solve the cube as fast as you can.
        UNDO: Reverse last move or last number of moves.

    Help sheets:
        NOTATION: Explain cube notation.
        METRICS: Explain different turn metrics.

    Cube attributes:
        CUBE: Return the cube state as a string.
        SIZE: Return cube size.
        MOVES: Return moves.
        SMOVES: Return scramble/setup moves.
        SHOWSTYLE: Return current style to show the cube.
        COLOURS: Return colour scheme of the cube in RGB.
    """
    os.system('cls')

    print("Virtual Cube Program - Made by Fred Lang.\n"
          "Enter HELP for list of functions.")

    cube = Cube()
    functions = [i for i in dir(cube) if callable(getattr(cube, i)) and not
                 i.startswith('_') and i != 'move' and i.islower()]
    cube.show()

    while True:
        try:
            screen_size = os.get_terminal_size().columns
        except (OSError, ValueError):
            screen_size = 80

        print('\n' + '=' * screen_size)
        moves = input("\nEnter move(s) or function: ").strip()

        if not moves:
            continue

        print()

        function = moves.split()[0].upper()
        if len(moves.split()) > 1:
            args = moves.split(maxsplit=1)[1]
        else:
            args = ''

        # Exit
        if function == 'EXIT':
            raise SystemExit

        # Help
        elif function == 'HELP':
            try:
                if args:
                    manual(args.upper())
                else:
                    manual()
            except FileNotFoundError as e:
                print(str(e).split(': ')[1], "was not found.")

        # Load
        elif function == 'LOAD':
            if args:
                filename = f'saves/{args}.txt'
            else:
                filename = 'saves/Cube.txt'

            try:
                cube = load(filename)
            except FileNotFoundError as e:
                print(str(e).split(': ')[1], "was not found.")
                continue

            print(f"Successfully loaded '{filename}'.")

            for name, moves in ('SCRAMBLE',cube.smoves), ('MOVES',cube.moves):
                if moves:
                    print(f"{name}: {' '.join(moves)}\n")
                else:
                    print(f"{name}: No moves\n")

            cube.show()

        # Save
        elif function == 'SAVE':
            if args:
                filename = f'saves/{args}.txt'
            else:
                i = 1
                while os.path.exists(f'saves/Cube {i}.txt'):
                    i += 1

                filename = f'saves/Cube {i}.txt'

            try:
                save(cube, filename)
            except FileNotFoundError:
                print("Could not create file.")
            else:
                print(f"Successfully saved as '{filename}'.")

        # Functions
        elif function.lower() in functions:
            if (function in {'PLAY', 'REPEAT'} or function == 'SCRAMBLE' and
                args[:5].upper() not in {'MOVES', 'STATE', 'SEED '}):
                try:
                    args = parse_moves(args)
                except MoveError as e:
                    print(e)
                    continue
            else:
                args = args.split()

            try:
                result = getattr(cube, function.lower())(*args)
            except (CubeError, MoveError) as e:
                print(e)
                continue
            except (TypeError, ValueError):
                print("Invalid arguments given.")
                continue
            except FileNotFoundError as e:
                print(str(e).split(': ')[1], "was not found.")
                continue

            if function in {'COLOUR', 'INPUT', 'INVERT', 'MIRROR', 'UNDO'}:
                cube.show()

            elif function == 'LINK':
                print(result)

            elif function == 'MOVECOUNT':
                for metric in result:
                    print(f"{metric}: {result[metric]}")

            elif function == 'REPEAT':
                if not result:
                    print(f"Did not solve.\n")
                elif result == 1:
                    print(f"Solved after 1 repetition.\n")
                else:
                    print(f"Solved after {result} repetitions.\n")
                cube.show()

            elif function == 'RESET':
                os.system('cls')
                print()
                cube.show()

            elif function == 'SCRAMBLE':
                if isinstance(result, list):
                    if result:
                        print(f"SCRAMBLE: {' '.join(result)}")
                        cube.reset(cube.size)
                        if cube.size:
                            print()
                            cube.show()
                            cube.play(*result)
                            cube.smoves = result
                            cube.moves = []
                    else:
                        print("SCRAMBLE: No moves")
                else:
                    print(f"SEED: {repr(result)}")

            elif function == 'SIMPLIFY':
                if result:
                    print(' '.join(result))
                else:
                    print("No moves.")

            elif function == 'SOLVE':
                solve, stats = result
                if isinstance(solve, int):
                    cube.show()
                    print(f"SOLVED: {solve}\n")

                    stats, solve_time = stats
                    table = [[], ['', 'AVERAGE', 'BEST', 'WORST']]

                    for substep in stats[0]:
                        if not isinstance(stats[0][substep], (int, float)):
                            continue

                        data = [movecount[substep] for movecount in stats]

                        if len(data) > 1:
                            mean = statistics.mean(data)
                            stdev = statistics.stdev(data)
                        else:
                            mean = data[0]
                            stdev = 0

                        if substep == 'HTM':
                            table.append([])

                        if substep == 'TIME':
                            table.append([])
                            average = f'{mean:.6f} (\u03c3={stdev:.2f})'
                            best = f'{min(data):.6f}'
                            worst = f'{max(data):.6f}'

                        else:
                            average = f'{mean:.3f} (\u03c3={stdev:.2f})'
                            best = f'{min(data)}'
                            worst = f'{max(data)}'

                        table.append([substep, average, best, worst])

                    table.append([])

                    if table[2]:
                        table.insert(2, [])

                    columns = zip(*[row for row in table if row])
                    columns = [len(max(column, key=len)) for column in columns]

                    line = ['', *('-' * column for column in columns), '']
                    line = '+'.join(line)

                    for y, row in enumerate(table):
                        if row:
                            for x, (i, length) in enumerate(zip(row, columns)):
                                if i and i[0].isalpha():
                                    table[y][x] = f'{i:^{length}}'
                                else:
                                    table[y][x] = f'{i:>{length}}'

                            table[y] = '|'.join(['', *table[y], ''])
                        else:
                            table[y] = line

                    table = '\n'.join(table)

                    print(table)
                    print(f"\nTOTAL TIME: {convert_seconds(solve_time)}")

                else:
                    if solve:
                        print(f"SOLUTION: {' '.join(solve)}")
                        cube.undo(len(solve))
                        cube.play(*solve)
                    else:
                        print("SOLUTION: No moves")

                    if len(stats) > 5:
                        print()

                    for stat in stats:
                        if stat in {'HTM', 'TIME'}:
                            print()
                        if stats[stat] == '':
                            print(f"{stat}: None")
                        elif stat == 'TIME':
                            print(f"{stat}: {stats[stat]:.6f}")
                        else:
                            print(f"{stat}: {stats[stat]}")

            elif function == 'SPEEDSOLVE':
                os.system('cls')
                print()
                cube.show()
                print()

                if not result['TIME'].startswith('D'):
                    print("Solved!")

                print(f"TIME: {result['TIME']}")
                print("\nMOVECOUNT:")
                for stat in 'HTM', 'QTM', 'STM', 'ETM':
                    print(f"{stat}: {result[stat]}")

                print()

                for stat in 'TPS', 'START TIME', 'END TIME':
                    print(f'{stat}: {result[stat]}')

        # Attributes
        elif function == 'CUBE':
            print(''.join(x for s in cube.cube for y in s for x in y))

        elif function == 'SIZE':
            print(cube.size)

        elif function == 'MOVES':
            if not cube.moves:
                print("No moves.")
            else:
                print(' '.join(cube.moves))

        elif function == 'SMOVES':
            if not cube.smoves:
                print("No moves.")
            else:
                print(' '.join(cube.smoves))

        elif function == 'SHOWSTYLE':
            for key, data in cube.show_style.items():
                print(f"{key}: {data}")

        elif function == 'COLOURS':
            for side, (r,g,b) in cube.colours.items():
                print(f"{side}: #{r:02x}{g:02x}{b:02x} or {r},{g},{b}")

        # Moves
        else:
            try:
                moves = parse_moves(moves)
                cube.move(moves)
            except MoveError as e:
                print(e)
            else:
                cube.show()


if __name__ == '__main__':
    try:
        freeplay()
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
