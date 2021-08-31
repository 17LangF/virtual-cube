"""Return current move count."""

from cube.functions import split_move


def movecount(self, metric: str = 'OVERVIEW') -> dict:
    """
    Return current move count.

    Parameters
    ----------
    metric : {'OVERVIEW', 'ALL', 'HTM', 'QTM', 'STM', 'ETM', 'QSTM',
    'ATM'}, optional
        If `metric` == 'OVERVIEW', the move counts using the main 4
        metrics (HTM, QTM, STM, ETM) are returned.

        If `metric` == 'ALL', the move counts in all 6 metrics (HTM,
        QTM, STM, ETM, QSTM, ATM) are returned.

        Else, only the move count specific to the metric is returned.

    Returns
    -------
    dict of {str: int}
        Movecounts of the cube in {`metric`: `move_count`} pairs.

    Notes
    -----
    HTM - Half Turn Metric or Outer Block Turn Metric
        In HTM a move can any outer turn.
        So U is 1HTM, U2 is 1HTM, M is 2HTM, M2 is 2HTM, and x is 0HTM.

    QTM - Quarter Turn Metric
        In QTM a move must be an outer quarter turn.
        So U is 1QTM, U2 is 2QTM, M is 2QTM, M2 is 4QTM, and x is 0QTM.

    STM - Slice Turn Metric or Block Turn Metric
        In STM a move can be any outer turn or slice move.
        So U is 1STM, U2 is 1STM, M is 1STM, M2 is 1STM, and x is 0STM.

    ETM - Execution Turn Metric
        In ETM a move can be any outer turn or slice move, and rotations
        are counted.
        So U is 1ETM, U2 is 1ETM, M is 1ETM, M2 is 1ETM, and x is 1ETM.

    QSTM - Quarter Slice Turn Metric
        In QTSM a move can be an outer quarter turn or quarter slice
        move.
        So U is 1QSTM, U2 is 2QTSM, M is 1QTSM, M2 is 2QTSM, and x is
        0QTSM.

    ATM - Axis Turn Metric
        In ATM a move can be any turn within the same axis.
        So U is 1ATM, U2 is 1ATM, M is 1ATM, M2 is 1ATM, x is 0ATM and L
        R is 1ATM.
    """
    if isinstance(metric, list):
        moves = metric
        metric = 'OVERVIEW'
    else:
        moves = self.moves

    metrics = 'HTM', 'QTM', 'STM', 'ETM', 'QSTM', 'ATM'
    move_counts = dict.fromkeys(metrics, 0)
    last_axis = 'X'

    for move in moves:
        depth, face, turns = split_move(move, self.size)

        if face in {'U', 'D'}:
            axis = 'U'
        elif face in {'L', 'R'}:
            axis = 'L'
        else:
            axis = 'F'

        # Rotations
        if move.startswith(('x', 'y', 'z')):
            move_counts['ETM'] += 1

        # Slice moves
        elif depth[0] != 0:
            move_counts['HTM'] += 2
            move_counts['QTM'] += abs(turns * 2)
            move_counts['STM'] += 1
            move_counts['ETM'] += 1
            move_counts['QSTM'] += abs(turns)
            move_counts['ATM'] += axis != last_axis

        # Outer turns
        else:
            move_counts['HTM'] += 1
            move_counts['QTM'] += abs(turns)
            move_counts['STM'] += 1
            move_counts['ETM'] += 1
            move_counts['QSTM'] += abs(turns)
            move_counts['ATM'] += axis != last_axis

        if face in {'U', 'D'}:
            last_axis = 'U'
        elif face in {'L', 'R'}:
            last_axis = 'L'
        else:
            last_axis = 'F'

    if metric.upper() in move_counts:
        metrics = [metric.upper()]

    elif metric.upper() == 'OVERVIEW':
        metrics = 'HTM', 'QTM', 'STM', 'ETM'

    elif metric.upper() == 'ALL':
        metrics = move_counts.keys()

    else:
        raise ValueError

    return {metric: move_counts[metric] for metric in metrics}
