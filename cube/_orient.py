'''
Virtual Cube Program - Made by Fred Lang.
Orient method.
'''

#Orient
def orient(self):
    size = self.size

    if size % 2:
        centre = size // 2
        centres = tuple(self.cube[s][centre][centre] for s in range(6))

        if {'U','F'}.issubset(centres):
            U = centres.index('U')
            F = centres.index('F')
        else:
            print(centres)
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
            vertex = tuple(self.cube[v[x][0]][v[x][1]][v[x][2]]
                          for x in range(3))

            if set(vertex) == set('DBL'):
                U = v[vertex.index('D')][0]
                F = v[vertex.index('B')][0]

                if U == 0:
                    U = 5
                elif U == 5:
                    U = 0
                else:
                    U = (U + 1) % 4 + 1

                if F == 0:
                    F = 5
                elif F == 5:
                    F = 0
                else:
                    F = (F + 1) % 4 + 1

    orientations = (
        (False, ["y'"], [], ['y'], ['y2'], False),
        (['z','y'], False, ['z'], False, ['z','y2'], ['z',"y'"]),
        (['x','y2'], ['x',"y'"], False, ['x','y'], False, ['x']),
        (["z'","y'"], False, ["z'"], False, ["z'",'y2'], ["z'",'y']),
        (["x'"], ["x'","y'"], False, ["x'",'y'], False, ["x'",'y2']),
        (False, ['x2',"y'"], ['z2'], ['x2','y'], ['x2'], False)
    )

    return orientations[U][F]
