"""Return help page for a given function."""


def manual(function: str = 'GENERAL'):
    """
    Print help page for a given function.

    Parameters
    ----------
    function : str, default='GENERAL'
        Requested help page.
    """
    with open('docs/manual.txt', encoding='utf-8') as f:
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
        print(f"No help page for {function}.")

    # SHOW examples
    if function == 'SHOW':

        from cube import Cube

        cube = Cube()
        examples = (
            ("Change mode to 2D", "2D"),
            ("Default SHOW function", ""),
            ("Letters in colour", "letters"),
            ("Letters with background of colour", "letters bg,colour"),
            ("Letters with no colour", "letters 0"),
            ("Letters in black, underlined, with background of colour",
             "letters fg,0,0,0,4,bg,colour"),
            ("Change letters to O", "O"),
            ("Blocks with foreground of colour and with no spaces",
             "block fg,colour False"),
            ("Show last style again", "")
        )

        print("\nSHOW 2D Examples:")
        for description, parameters in examples:
            print()
            print(description)
            print('SHOW',  parameters)
            print()
            cube.show(*parameters.split())

    # INPUT examples
    elif function == 'INPUT':

        from cube import Cube

        cube = Cube()
        examples = (
            ("Solved",
             "UUUUUUUUULLLLLLLLLFFFFFFFFFRRRRRRRRRBBBBBBBBBDDDDDDDDD"),
            ("Checker board pattern",
             "UDUDUDUDULRLRLRLRLFBFBFBFBFRLRLRLRLRBFBFBFBFBDUDUDUDUD"),
            ("Six spot pattern",
             "UUUUFUUUULLLLDLLLLFFFFRFFFFRRRRURRRRBBBBLBBBBDDDDBDDDD"),
            ("Superflip pattern",
             "UBULURUFULULBLFLDLFUFLFRFDFRURFRBRDRBUBRBLBDBDFDLDRDBD"),
            ("Cube in a cube in a cube pattern",
             "UUUUFFUFRLLLDDLBDLFRUFRRFFFFURUURRRRBBBBLLBLDDDDBBDLBD")
        )

        print("\nExamples:")
        for description, parameters in examples:
            print()
            print(description)
            print("INPUT",  parameters)
            print()
            if description == 'Solved':
                cube.show('2D')
                continue
            cube.input(parameters)
            cube.show()
