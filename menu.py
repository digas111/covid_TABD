import curses

menu = ['Home','Play','Scoreboard','Exit']

def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()


    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    
    stdscr.refresh()



def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    current_row_idx = 0

    print_menu(stdscr, current_row_idx)
    
    while 1:
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
            stdscr.addstr(0, 0, "You pressed Up key!")
        elif key == curses.KEY_DOWN and current_row_idx < len(menu)-1:
            current_row_idx += 1
            stdscr.addstr(0, 0, "You pressed Down Key!")
        elif key == curses.KEY_ENTER or key in [10,13]:
            # stdscr.addstr(0, 0, "You pressed {}".format(menu[current_row_idx]))
            # stdscr.refresh()
            # stdscr.getch()
            if (current_row_idx == len(menu)-1):
                exit(0)

        print_menu(stdscr, current_row_idx)
        stdscr.refresh()

curses.wrapper(main)