from __future__ import absolute_import, unicode_literals
import curses
from curses import panel
from pytify.strategy import get_pytify_class_by_platform

class SongList():
    def __init__(self, items):
        self.pytify = get_pytify_class_by_platform()()
        self.items = items

        self.position = 2
        self.song_length = len(items) - 1

        # Init curses screen
        self.window = curses.initscr()

        self.window.keypad(1)

        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()

        # Show shortcuts
        self.shortcuts()

        # Disable blinking cursor
        curses.curs_set(False)

        # Display window
        self.display()

    def shortcuts(self):
        self.items.append(' ')
        self.items.append('Keyboard shortcuts')
        self.items.append('==================')
        self.items.append('Navigation (Vim bindings):')
        self.items.append('  <K> <up> ')
        self.items.append('  <J> <down> ')
        self.items.append('  <H> <left> ')
        self.items.append('  <L> <right> ')
        self.items.append('Play: <P>')
        self.items.append('Search: <S>')
        self.items.append('Play/Pause: <SPACEBAR>')


    def navigate(self, n):
        self.position += n

        if self.position < 2:
            self.position = 2
        elif self.position > self.song_length:
            self.position = self.song_length

    def display(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()

        while True:
            self.window.refresh()
            curses.doupdate()

            for index, item in enumerate(self.items):
                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL

                self.window.addstr(index, 1, str(item), mode)

            key = self.window.getch()

            # Start song
            if key == ord('p'):
                self.pytify.listen(int(self.position - 1))

            # Up
            elif key == ord('k'):
                self.navigate(-1)

            # Down
            elif key == ord('j'):
                self.navigate(1)

            # Left
            elif key == ord('h'):
                self.pytify.prev()

            # Rights
            elif key == ord('l'):
                self.pytify.next()

            # Play/Pause
            elif key == ord(' '):
                self.pytify.play_pause()

            # Search
            elif key == ord('s'):
                break

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()