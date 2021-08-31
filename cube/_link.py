"""Return an alg.cubing.net link for the cube."""


def link(self) -> str:
    """
    Return an alg.cubing.net link for the cube.

    Size must be from 1x1 to 17x17 to be supported by alg.cubing.net.

    Returns
    -------
    str
        alg.cubing.net link.

    Raises
    ------
    CubeError
        If size is not supported by alg.cubing.net.
    """

    from cube import CubeError

    size = self.size
    smoves = self.smoves
    moves = self.moves
    parameters = []
    replacements = (
        ('-', '%26%2345%3B'),
        ('[', '%5B'),
        (']', '%5D'),
        ("'", '-')
    )

    if not 0 < size < 18:
        raise CubeError("Size is not supported by alg.cubing.net.")

    if size != 3:
        size = 'x'.join([str(size)]*3)
        parameters.append(f'puzzle={size}')

    if smoves:
        smoves = '_'.join(smoves)
        for a, b in replacements:
            smoves = smoves.replace(a, b)
        parameters.append(f'setup={smoves}')

    if moves:
        moves = '_'.join(moves)
        for a, b in replacements:
            moves = moves.replace(a, b)
        parameters.append(f'alg={moves}')

    url = 'https://alg.cubing.net/'
    if not parameters:
        return url
    parameters = '&'.join(parameters)
    return f'{url}?{parameters}'
