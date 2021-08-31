"""Reset cube and set cube size."""


def reset(self, size='ALL'):
    """
    Reset cube and set cube size.

    Some functions may become very slow if the cube is too large.

    Parameters
    ----------
    size : int or str, default='ALL'
        Number of cubies on each edge of the cube.

        If `size` == 'ALL', all attributes of the cube are reset.

        Else, `size` must be an integer or numeric string and only
        `cube.cube`, `cube.moves` and `cube.smoves` are reset.
    """
    if isinstance(size, str):
        if size.upper() == 'ALL':
            self.__init__()
            return

        if not size.isdecimal():
            raise ValueError
        size = int(size)

    self.cube = [[[i]*size for _ in range(size)] for i in 'ULFRBD']
    self.moves = []
    self.smoves = []

    if size != self.size:
        self.size = size
        zoom = self.show_style['3D'][3]
        self.show_style['3D'][4] = abs(zoom) / (5 * size + 5)
