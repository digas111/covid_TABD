# Simple bar value interface
#
import curses
import time
 
# get_io is using random values, but a real I/O handler would be here
def get_io():
    import random
    global value1
    value1 = random.randint(1,30)
 
bar = '█' # an extended ASCII 'fill' character
stdscr = curses.initscr()
height, width = stdscr.getmaxyx() # get the window size
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
 
# add some labels
stdscr.addstr(4,1, "Pi Sensor 1 :")
 
# Define windows to be used for bar charts
win1 = curses.newwin(3, 32, 3, 15) # curses.newwin(height, width, begin_y, begin_x)
 
# Use the 'q' key to quit
k = 0
while (k != ord('q')):
    get_io() # get the data values
    win1.clear()
    win1.border(0)
# create bars bases on the returned values
    win1.addstr(1, 1, bar * value1, curses.color_pair(1))
    win1.refresh()
# add numeric values beside the bars
    stdscr.addstr(4,50, str(value1) + " Deg ",curses.A_BOLD )
    stdscr.refresh()
    time.sleep(2)
    stdscr.nodelay(1)
    k = stdscr.getch() # look for a keyboard input, but don't wait
 
curses.endwin() # restore the terminal settings back to the original
