"""Create a command line interface to play moves one at a time."""

import time


def play(self, *moves: str):
    """
    Create a command line interface to play moves one at a time.

    Enter key - step through the moves one at a time.

    EXIT or Ctrl+C - skip to the end of the moves.

    PLAY tps - animate the moves (should only be used in 3D SHOW mode).
        Default tps = size ^ 2 / 2 + 1.

        If tps is 0, the moves are played at maximum speed.

        If tps is xN, the moves are played N times the default speed.

    Parameters
    ----------
    *moves : str
        Sequence of moves to be excecuted in order.

    Raises
    ------
    MoveError
        If any of the moves are invalid.
    """
    size = self.size
    play = False
    move_time = 0

    i = 0
    try:
        while i < len(moves):
            if not play:
                choice = input().strip().upper()

                if not choice:
                    print(moves[i])

                elif choice == 'EXIT':
                    self.move(moves[i:])
                    self.show()
                    break

                elif choice.split()[0] == 'PLAY':
                    if choice == 'PLAY':
                        tps = size ** 2 / 2 + 1
                    else:
                        tps = choice.split(maxsplit=1)[1]
                        if tps[0].lower() == 'x':
                            if tps[1:].replace('.', '', 1).isdecimal():
                                tps = float(tps[1:]) * (size ** 2 / 2 + 1)
                            else:
                                print("Invalid tps.")
                                continue

                        elif tps.replace('.', '', 1).isdecimal():
                            tps = float(tps)

                        else:
                            print("Invalid tps.")
                            continue

                    play = True
                    if tps > 0:
                        move_time = 1 / tps
                    else:
                        move_time = 0

                else:
                    print("Invalid function.")
                    continue

            self.move(moves[i])
            self.show()
            i += 1
            time.sleep(move_time)

    except (EOFError, KeyboardInterrupt):
        self.move(moves[i:])
        self.show()
