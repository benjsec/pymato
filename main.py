import collections
import curses
# import logging
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
    """A timer class that encapuslates the main functionality of the program.

    :param stdscr: The curses screen to display updates on.
    """


    # Currently the seconds are measured by waiting for the key presses, this
    # may want to be updated to look at start and end time... but for now this
    # works well enough.
    SECOND = 1000

    def __init__(self, stdscr):
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
        """Make a "ding" noise"""
        p = subprocess.PIPE
        p1 = subprocess.Popen(
            ["ffplay", "-nodisp", "-autoexit", "complete.wav"],
            stdout=p, stderr=p)

    def add_phase(self, name, duration):
        """Add a phase to the list of phases to cycle through.

        :param name: The name of the phase, to be shown when in progress.
        :param duration: The length of the phase, in seconds.
        """
        phase = Phase(name, duration)
        self.phases.append(phase)

    def end_phase(self):
        """To be called at the end of a phase.

        This will display the end-of-phase message to the user, and wait for
        a key to be pressed before continuing.
        """
        self.ding()
        self.win.clear()
        self.disp_phase("End of {} phase", self.current_phase)
        self.disp_time("Press any key to begin next phase.")
        self.wait()
        self.win.clear()

    def disp_phase(self, fmt, *args):
        """Update the line where the current phase is displayed.

        :param fmt: A string format specification
        :param args: Any arguments needed for the string formatting.
        """
        self.win.addstr(0, 2, fmt.format(*args).ljust(self.maxx))
        self.win.refresh()

    def disp_time(self, fmt, *args):
        """Update the line where the time remaining is displayed.

        :param fmt: A string format specification
        :param args: Any arguments needed for the string formatting.
        """
        self.win.addstr(2, 2, fmt.format(*args).ljust(self.maxx))
        self.win.refresh()

    def wait(self, timeout=-1):
        """Wait until a key is pressed, or timeout, and return the key.

        :param timeout: Time to wait for a key press in milliseconds. If not
            given or -1 will wait forever.
        :returns: The key pressed, or `None` if no key was pressed.
        """
        self.stdscr.timeout(timeout)
        try:
            key = self.stdscr.getkey()
        except curses.error:
            key = None
        else:
            key = key.lower()
        finally:
            self.stdscr.timeout(self.SECOND)
        return key

    def period(self, phase):
        """Begin a new phase period.

        :param phase: The new phase period to move into. Must be a namedtuple
            `Phase` object.
        """
        self.current_phase = phase.name
        self.disp_phase("You should currently be {}", phase.name)
        self.time(phase.duration)

    def pause(self):
        """Pause the timer until a key is pressed"""
        self.disp_time("Timer paused, press any key to resume.")
        self.wait()

    def time(self, length):
        """Time a length of seconds, and update the screen as it progresses.

        :param length: The time in seconds to count for.
        """
        if length < 0:
            raise ValueError(
                "Length of phase must be positive, got {}".format(length))
        for i in range(length, 0, -1):
            self.disp_time("Time remaining: {}",
                time.strftime("%M:%S", time.gmtime(i)))
            key = self.wait(self.SECOND)
            if key == 'q':  # Quit completely
                raise ExitException
            elif key == 's':  # Skip phase
                break
            elif key == ' ':  # Pause
                self.pause()
        else:
            self.end_phase()

    def run(self, repeat=1):
        """Run the timer with the phases currently added.

        :param repeat: The number of times to repeat the phases cycle.
        """
        for x in range(repeat):
            for phase in self.phases:
                self.period(phase)


def main(stdscr):
    """Create the timer, add the phases and run the timer."""
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