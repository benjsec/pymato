import collections
import curses
import math
import subprocess
import time


Phase = collections.namedtuple("Phase", ["name", "duration"])


phases = [Phase('working', 20*60), Phase('resting', 5*60)]


class ExitException(Exception):
    """Exception to raise when exiting nicely"""


class Timer:

    SECOND = 1000

    def __init__(self, stdscr, phases=None):
        self.stdscr = stdscr
        self.stdscr.timeout(self.SECOND)
        self.phases = phases or []
        self.current_phase = None
        self.stdscr.addstr(0, 0, " ~~ Pymato Timer ~~ ")
        # self.stdscr.addstr(-1, 0, "Instructions go here")

    def ding(self):
        p = subprocess.PIPE
        p1 = subprocess.Popen(
            ["ffplay", "-nodisp", "-autoexit", "complete.wav"],
            stdout=p, stderr=p)

    def add_phase(self, name, duration):
        self.phases += Phase(name, duration)

    def end_phase(self):
        self.ding()
        self.stdscr.addstr(
            2, 0, "End of {} phase".format(self.current_phase).ljust(80))
        self.stdscr.addstr(
            3, 0, "Press any key to begin next phase.".ljust(80))
        self.stdscr.addstr(4, 0, "".ljust(80))
        self.stdscr.refresh()
        self.wait_forever()
        for i in range(2, 5):
            self.stdscr.addstr(i, 0, "".ljust(80))

    def wait_forever(self):
        self.stdscr.timeout(-1)
        self.stdscr.getkey()
        self.stdscr.timeout(self.SECOND)

    def period(self, phase):
        self.current_phase = phase.name
        self.stdscr.addstr(
            2, 0, "You should currently be {}".format(phase.name).ljust(80))
        self.time(phase.duration)

    def pause(self):
        self.stdscr.addstr(
                4, 0, "Timer paused".ljust(80))
        self.stdscr.refresh()
        self.wait_forever()


    def time(self, length):
        if length < 0:
            raise ValueError(
                "Length of phase must be positive, got {}".format(length))
        for i in range(length, 0, -1):
            m, s = math.floor(i/60), int(i%60)
            self.stdscr.addstr(
                4, 0, "Time remaining: {:0>2}:{:0>2}".format(m, s).ljust(80))
            self.stdscr.refresh()
            try:
                key = self.stdscr.getkey()
            except curses.error:
                pass
            else:
                if key == 'q':
                    raise ExitException
                elif key == 's':
                    break
                elif key == " ":
                    self.pause()
        else:
            self.end_phase()

    def run(self, repeat=1):
        for x in range(repeat):
            for phase in phases:
                self.period(phase)


def main(stdscr):
    timer = Timer(stdscr, phases)
    timer.run(4)


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except (ExitException, KeyboardInterrupt):
        pass