'''
Virtual Cube Program - Made by Fred Lang.
Play method.
'''

import time

#Play
def play(self, *moves):
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
                            if tps[1:].replace('.','',1).isdigit():
                                tps = float(tps[1:]) * (size ** 2 / 2 + 1)
                            else:
                                print('Invalid tps.')
                                continue

                        elif tps.replace('.','',1).isdigit():
                            tps = float(tps)

                        else:
                            print('Invalid tps.')
                            continue

                    play = True
                    if tps > 0:
                        move_time = 1 / tps
                    else:
                        move_time = 0

                else:
                    print('Invalid function.')
                    continue

            self.move(moves[i])
            self.show()
            i += 1
            time.sleep(move_time)

    except (EOFError, KeyboardInterrupt):
        self.move(moves[i:])
        self.show()
