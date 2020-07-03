import curses
import time


ninfectedBeforeMask = 0

title1 = "Primeiros infetados:"
menu1 = ['Porto & Lisboa','Porto','Lisboa','Exit']


title2 = "Utilização de máscara:"
menu2 = ['Sim','Não','Exit']

title3 = "Nº infetados antes de inicio de medidas:"


def print_menu1(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    x = w//2 - len(title1)//2
    y = h//3

    stdscr.addstr(y, x, title1)

    for idx, row in enumerate(menu1):
        x = w//2 - len(row)//2
        y = h//2 - len(menu1)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    
    stdscr.refresh()

def my_raw_input(stdscr, r, c, prompt_string):
    curses.echo() 
    stdscr.addstr(r, c, prompt_string)
    stdscr.refresh()
    input = stdscr.getstr(r + 1, c, 20)
    return input  #       ^^^^  reading input at next line  

def print_menu2(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    x = w//2 - len(title2)//2
    y = h//3

    stdscr.addstr(y, x, title2)

    for idx, row in enumerate(menu2):
        x = w//2 - len(row)//2
        y = h//2 - len(menu2)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    
    stdscr.refresh()

def print_menu3(stdscr):
    global ninfectedBeforeMask
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w//2 - len(title3)//2
    y = h//3

    curses.echo() 
    stdscr.addstr(y, x, title3)
    stdscr.refresh()
    x = w//2
    ninfectedBeforeMask = int(stdscr.getstr(y + 2, x, 20))



def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    current_row_idx = 0

    print_menu1(stdscr, current_row_idx)
    
    while 1:
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu1)-1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10,13]:
            
            if (current_row_idx == 0):
                #Porto & Lisboa
                break
            elif (current_row_idx == 1):
                break
                #Porto

            elif (current_row_idx == 2):
                #Lisboa
                break

            elif (current_row_idx == len(menu1)-1):
                exit(0)

        print_menu1(stdscr, current_row_idx)
        stdscr.refresh()


    print_menu2(stdscr, current_row_idx)

    while 1:
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu2)-1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10,13]:

            if (current_row_idx == 0):
                print_menu3(stdscr)
                
                break
            elif (current_row_idx == 1):
                #Não
                break
           
            elif (current_row_idx == len(menu2)-1):
                exit(0)

        print_menu2(stdscr, current_row_idx)
        stdscr.refresh()

    print(ninfectedBeforeMask)
    time.sleep(3)

    # exit(0)

curses.wrapper(main)