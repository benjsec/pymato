import collections
import curses
# import logging
import math
import subprocess
import time


# def setup_log():
#     """Create a logger, configure and return it."""
#     logger = logging.getLogger('Timer')
#     logger.setLevel(logging.DEBUG)
#     formatter = logging.Formatter("[%(levelname)7s] %(message)s")
#     handler = logging.FileHandler("timer.log")
#     handler.setFormatter(formatter)
#     logger.addHandler(handler)
#     return logger, handler


# log, handler = setup_log()       # pylint: disable=invalid-name


Phase = collections.namedtuple("Phase", ["name", "duration"])


class ExitException(Exception):
    """Exception to raise when exiting nicely"""


class Timer:

    SECOND = 1000

    def __init__(self, stdscr, phases=None):
        self.stdscr = stdscr
        self.stdscr.timeout(self.SECOND)
        self.phases = []
        self.current_phase = None
        self.maxy, self.maxx = stdscr.getmaxyx()
        self.stdscr.addstr(0, 0, " ~~ Pymato Timer ~~ ".center(self.maxx))
        self.stdscr.addstr(self.maxy-1, 2,
                           "Space: Pause\t s: Skip phase\t q: Quit")
        self.win = self.stdscr.subwin(3, 0)

    def ding(self):
        p = subprocess.PIPE
        p1 = subprocess.Popen(
            ["ffplay", "-nodisp", "-autoexit", "complete.wav"],
            stdout=p, stderr=p)

    def add_phase(self, name, duration):
        phase = Phase(name, duration)
        self.phases.append(phase)

    def end_phase(self):
        self.ding()
        self.win.cls()
        self.disp_phase("End of {} phase", self.current_phase)
        self.disp_time("Press any key to begin next phase.")
        self.wait_forever()
        self.win.cls()

    def disp_phase(self, fmt, *args):
        self.win.addstr(0, 2, fmt.format(*args).ljust(self.maxx))
        self.win.refresh()

    def disp_time(self, fmt, *args):
        self.win.addstr(2, 2, fmt.format(*args).ljust(self.maxx))
        self.win.refresh()

    def wait_forever(self):
        self.stdscr.timeout(-1)
        self.stdscr.getkey()
        self.stdscr.timeout(self.SECOND)

    def period(self, phase):
        self.current_phase = phase.name
        self.disp_phase("You should currently be {}", phase.name)
        self.time(phase.duration)

    def pause(self):
        self.disp_time("Timer paused, press SPACE to resume.")
        self.wait_forever()

    def get_key(self):
        try:
            key = self.stdscr.getkey()
        except curses.error:
            return None
        else:
            return key.lower()

    def time(self, length):
        if length < 0:
            raise ValueError(
                "Length of phase must be positive, got {}".format(length))
        for i in range(length, 0, -1):
            m, s = math.floor(i/60), int(i%60)
            self.disp_time("Time remaining: {:0>2}:{:0>2}", m, s)
            # self.win.addstr(
            #     2, 0, "Time remaining: {:0>2}:{:0>2}".format(m, s).ljust(80))
            # self.win.refresh()
            key = self.get_key()
            if key == 'q':
                raise ExitException
            elif key == 's':
                break
            elif key == ' ':
                self.pause()
        else:
            self.end_phase()

    def run(self, repeat=1):
        for x in range(repeat):
            for phase in self.phases:
                self.period(phase)


def main(stdscr):
    timer = Timer(stdscr)
    timer.add_phase("working", 20*60)
    timer.add_phase("resting", 5*60)
    timer.run(4)


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except (ExitException, KeyboardInterrupt):
        pass
    finally:
        pass