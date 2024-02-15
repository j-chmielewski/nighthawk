import curses

from nighthawk import NightHawkData


BARS = {
    0: '     ',
    1: '▁    ',
    2: '▁▂   ',
    3: '▁▂▃  ',
    4: '▁▂▃▄ ',
    5: '▁▂▃▄▅',
}
METRIC_BOUNDS = {
    'sinr': [-5, 20],
    'rsrp': [-100, -80],
    'rsrq': [-20,  -10],
    'rssi': [-90, -55],
}
PROGRESS_FULL = '█'
PROGRESS_EMPTY = '▒'


class Gui:

    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.initscr()
        curses.start_color()
        self._init_colors()

    def update(self, data: NightHawkData):
        self.stdscr.clear()
        # bars
        bars_str = f'[{BARS[data.bars]}]'
        self.stdscr.addstr(0, 0, bars_str, self._bars_color(data.bars))

        # network
        self.stdscr.addstr(0, 8, data.network)

        # connection type
        self.stdscr.addstr(0, 9 + len(data.network), f'({data.connection})')

        # signal
        for i, metric in enumerate(['rssi', 'sinr', 'rsrp', 'rsrq']):
            percent = self._metric_percent(metric, data.__getattribute__(metric))
            color = self._percent_color(percent)
            bars = self._bars(percent)
            line = f'{metric.upper()} {bars} {data.__getattribute__(metric):4d} ({percent}%)'
            self.stdscr.addstr(i+1, 0, line, color)

        self.stdscr.refresh()

    @staticmethod
    def _init_colors():
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    @staticmethod
    def _bars_color(bars: int):
        if bars <= 1:
            return curses.color_pair(1)
        if bars <= 3:
            return curses.color_pair(2)
        if bars <= 5:
            return curses.color_pair(3)

    @staticmethod
    def _metric_percent(metric_name: str, metric_value: int):
        bounds = METRIC_BOUNDS[metric_name]
        percent = (metric_value - bounds[0]) / (bounds[1] - bounds[0])
        percent = int(100 * percent)
        percent = max(0, min(100, percent))
        return percent

    @staticmethod
    def _percent_color(percent: int):
        if percent <= 33:
            return curses.color_pair(1)
        elif percent <= 66:
            return curses.color_pair(2)
        else:
            return curses.color_pair(3)

    @staticmethod
    def _bars(percent: int):
        full = round(percent / 10)
        return PROGRESS_FULL * full + PROGRESS_EMPTY * (10 - full)
