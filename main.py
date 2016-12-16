import collections
import math
import subprocess
import time
from curses import wrapper


Phase = collections.namedtuple("Phase", ["name", "duration"])


phases = [Phase('working', 20*60), Phase('resting', 5*60)]


class Timer:
    def __init__(self, stdscr, phases=None):
        self.stdscr = stdscr
        self.phases = phases or []
        self.current_phase = None
        self.stdscr.addstr(0, 0, " ~~ Pomato Timer ~~ ")
        # self.stdscr.addstr(-1, 0, "Instructions go here")

    def ding(self):
        p = subprocess.PIPE
        p1 = subprocess.Popen(
            ["ffplay", "-nodisp", "-autoexit", "complete.wav"],
            stdout=p, stderr=p)

    def add_phase(self, name, duration):
        self.phases += Phase(name, duration)

    def wait(self):
        self.stdscr.addstr(
            2, 0, "End of {} phase".format(self.current_phase).ljust(80))
        self.stdscr.addstr(
            3, 0, "Press any key to begin next phase.".ljust(80))
        self.stdscr.addstr(4, 0, "".ljust(80))
        self.stdscr.refresh()
        self.stdscr.getkey()
        for i in range(2, 5):
            self.stdscr.addstr(i, 0, "".ljust(80))

    def period(self, phase):
        self.current_phase = phase.name
        self.stdscr.addstr(
            2, 0, "You should currently be {}".format(phase.name).ljust(80))
        self.time(phase.duration)

    def time(self, length):
        if length < 0:
            raise ValueError(
                "Time to wait must be positive, got {}".format(length))
        for i in range(length, 0, -1):
            m, s = math.floor(i/60), int(i%60)
            self.stdscr.addstr(
                4, 0, "Time remaining: {:0>2}:{:0>2}".format(m, s).ljust(80))
            self.stdscr.refresh()
            time.sleep(1)
        else:
            self.ding()
            self.wait()

    def run(self, repeat=1):
        for x in range(repeat):
            for phase in phases:
                self.period(phase)


def main(stdscr):
    timer = Timer(stdscr, phases)
    timer.run(4)


if __name__ == "__main__":
    try:
        wrapper(main)
    except KeyboardInterrupt:
        pass