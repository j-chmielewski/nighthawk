import argparse
import curses
import time

from nighthawk import NightHawk
from ui import Gui


def main(stdscr, user, password, address):
    gui = Gui(stdscr)
    nh = NightHawk(user=user, password=password, address=address)
    while True:
        data = nh.get_data()
        gui.update(data)
        time.sleep(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', type=str, default='admin')
    parser.add_argument('-p', '--password', type=str)
    parser.add_argument('-a', '--address', type=str, default='http://192.168.1.1')
    args = parser.parse_args()

    curses.wrapper(main, args.user, args.password, args.address)
