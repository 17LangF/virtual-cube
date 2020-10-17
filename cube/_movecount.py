'''
Virtual Cube Program - Made by Fred Lang.
Movecount method.
'''

from cube.functions import split_move

#Movecount
def movecount(self, metric='OVERVIEW'):
    size = self.size
    moves = self.moves

    metrics = ('HTM','QTM','STM','ETM','QSTM','ATM','OBTM','BTM')
    move_counts = dict.fromkeys(metrics, 0)

    last_axis = 'X'

    for move in moves:
        depth, face, turns = split_move(move, size)

        if face in 'UD':
            axis = 'U'
        elif face in 'LR':
            axis = 'L'
        else:
            axis = 'F'

        #Rotations
        if move[0] in 'xyz':
            move_counts['ETM'] += 1

        #Slice moves
        elif depth[0] != 0:
            move_counts['HTM'] += 2
            move_counts['QTM'] += abs(turns * 2)
            move_counts['STM'] += 1
            move_counts['ETM'] += 1
            move_counts['QSTM'] += abs(turns)
            move_counts['ATM'] += axis != last_axis
            move_counts['OBTM'] += 2
            move_counts['BTM'] += 1

        #Outer turns
        else:
            move_counts['HTM'] += 1
            move_counts['QTM'] += abs(turns)
            move_counts['STM'] += 1
            move_counts['ETM'] += 1
            move_counts['QSTM'] += abs(turns)
            move_counts['ATM'] += axis != last_axis
            move_counts['OBTM'] += 1
            move_counts['BTM'] += 1

        if face in 'UD':
            last_axis = 'U'
        elif face in 'LR':
            last_axis = 'L'
        else:
            last_axis = 'F'

    if metric.upper() in move_counts:
        metrics = [metric.upper()]

    elif metric.upper() == 'OVERVIEW':
        metrics = ('HTM','QTM','STM','ETM')

    elif metric.upper() == 'ALL':
        metrics = move_counts.keys()

    else:
        raise TypeError

    return {metric: move_counts[metric] for metric in metrics}
