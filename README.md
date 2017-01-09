# Pymato Timer

This is a simple timer written in python to aid with the pomodoro technique.
It provides an alternating pattern of 20 and 5 minute periods, with an audible
bell after each phase. At the end of the phase the timer will not automatically
progress to the next phase, but wait to be triggered. This avoids your break
being used up whilst you just finish a little bit of work (or vice versa).

It is written in python 3.5 and uses only the standard libraries.

## Controls

Whilst the timer is running the following controls can be used:

* `SPACE` This will pause the timer, pressing any key will resume it.
* `s` Skip the current phase and being the next phase immediately.
* `q` Exit the timer.


## Development requirements:

* Pytest

## TODO

### Unit and functional tests

Perhaps the most boring step, but one of the most important, which is why it is
at the top of this list. Currently there are no tests at all for this project,
which is something of a travesty. It should strive for 100% test coverage, with
a full set of unit and functional tests. CI testing (via Travis) is also
envisaged.

### Customisation

The periods (alternating 20 minutes and 5 minutes repeating 4 times) cannot be
altered without modifying the code. A later version will provide a config file
that these values can be specified in. This will include the names and lengths
of the periods, with an unlimited number of periods being permitted.

### Auto advance

Whilst I prefer the timer not to advance to the next phase automatically, some
people do not like this behaviour. A setting in the customisation file will be
included to enable auto advancing between phases.

### Dynamic UI

* ~~UI should resize when the window is resized~~
* Control hints should hide when not relevant (e.g. between phases)
* Quit (q) should still work between phases (and hint should show).
* Crashing the program should not mess up the terminal (it does a bit at the 
    moment).
* Handle display-too-small scenario


### Desktop notifications

Ideally the system should be able to link into the OS system notificaiton panel
and provide a system desktop notification to indicate when a phase has ended.
Do no expect this feature soon, but it is on the roadmap.
