import curses
from unittest.mock import MagicMock

import pytest

import pymato

class TestWindow:

    @pytest.fixture
    def curses(self, monkeypatch):
        mock_curses = MagicMock(curses)
        monkeypatch.setattr("pymato.curses", mock_curses)
        return mock_curses

    def test_init(self):
        win = pymato.Window()
        assert win.scr is None

    def test_context(self, curses):
        with pymato.Window() as win:
            scr = win.scr
            assert scr is not None
            assert curses.noecho.called
            assert curses.cbreak.called
            assert scr.keypad.called_with(True)
            assert scr.timeout.called_with(win.SECOND)
        assert scr.keypad.called_with(False)
        assert curses.nocbreak.called
        assert curses.echo.called
        assert curses.endwin.called


class TestTimer:

    @pytest.fixture
    def scr(self):
        return MagicMock(curses.initscr())

    def test_init(self, scr):
        timer = pymato.Timer(scr)
        assert not timer.phases
        assert timer.current_phase is None