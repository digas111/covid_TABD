import curses
import os

# Formating for progress bars
suffix = '%(percent)d%% | %(elapsed_td)s'

# Text for the progress bars

offstestext =                "Reading offsets ...................."
simulatevirustext =          "Simulating virus propagation ......."
infectedbydistricttext =     "Getting infected by district ......."
savesimulateinfectiontext =  "Saving simulateInfection ..........."
saveNInfectedtext =          "Saving nº Infections ..............."
saveRtext =                  "Saving R values ...................."
saveInfectedByDistricttext = "Saving infectionsByDistrict ........"
saveInfectedByDistricttext = "Saving infectedByDistrict .........."

#Text for enlapsed time
enlapsedtimetext = "Files generated in: "

def print_menu(stdscr, selected_row_idx, title, menuItems):

    stdscr.clear()
    h, w = stdscr.getmaxyx()

    x = w//2 - len(title)//2
    y = h//3

    stdscr.addstr(y, x, title)

    for idx, row in enumerate(menuItems):
        x = w//2 - len(row)//2
        y = h//2 - len(menuItems)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    
    stdscr.refresh()


def getStartingOptions(stdscr):

    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    title = "Primeiros infetados:"
    menuItems = ['Porto & Lisboa','Porto','Lisboa','Exit']

    current_row_idx = 0

    print_menu(stdscr, current_row_idx, title, menuItems)
    
    while 1:
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menuItems)-1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10,13]:
            
            if (current_row_idx == 0):
                #Porto & Lisboa
                return 1
            elif (current_row_idx == 1):
                #Porto
                return 2
            elif (current_row_idx == 2):
                #Lisboa
                return 3
            elif (current_row_idx == len(menuItems)-1):
                return 0

        print_menu(stdscr, current_row_idx, title, menuItems)
        stdscr.refresh()


def precautionaryMeasures(stdscr):

    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    title = "Medidas de precaução:"
    menuItems = ['Sim','Não','Exit']

    current_row_idx = 1

    print_menu(stdscr, current_row_idx, title, menuItems)

    while 1:
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menuItems)-1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10,13]:

            if (current_row_idx == 0):
                #Sim
                infectedBeforeMeasures = getInfectedBeforeMeasures(stdscr)
                return infectedBeforeMeasures
            
            elif (current_row_idx == 1):
                #Não
                return -1
           
            elif (current_row_idx == len(menuItems)-1):
                return -2

        print_menu(stdscr, current_row_idx, title, menuItems)
        stdscr.refresh()


def getInfectedBeforeMeasures(stdscr):

    title = "Nº infected before taking measures:"

    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w//2 - len(title)//2
    y = h//3

    curses.echo() 
    stdscr.addstr(y, x, title)
    stdscr.refresh()
    x = w//2
    return int(stdscr.getstr(y + 2, x, 20))


# Menus for tracks_animation

# dir_path = os.path.dirname(os.path.realpath(__file__)) + "/data/"

# print(dir_path)

# startingOptions = os.listdir(dir_path)

# if '.DS_Store' in startingOptions:
#     startingOptions.remove('.DS_Store')

# print(startingOptions)

def chooseInfectionStart(stdscr, path):

    startingOptions = [name for name in os.listdir(path) if os.path.isdir(path + "/" + name)]

    if '.DS_Store' in startingOptions:
        startingOptions.remove('.DS_Store')

    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    title = "Choose Infection starting point:"

    current_row_idx = 0

    print_menu(stdscr, current_row_idx, title, startingOptions)
    
    while 1:
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(startingOptions)-1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10,13]:

            if current_row_idx == len(startingOptions)-1:
                return 0

            else:
                return startingOptions[current_row_idx] + "/"
            

        print_menu(stdscr, current_row_idx, title, startingOptions)
        stdscr.refresh()

def chooseMeasures(stdscr, path):

    startingMeasures = [name for name in os.listdir(path) if os.path.isdir(path + "/" + name)]

    if '.DS_Store' in startingMeasures:
        startingMeasures.remove('.DS_Store')

    if startingMeasures == []:
        return -1

    menuItems = ['No Measures'] + startingMeasures + ['Exit']

    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    title = "Nº infected before taking measures:"

    current_row_idx = 0

    print_menu(stdscr, current_row_idx, title, menuItems)
    
    while 1:
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menuItems)-1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10,13]:
            if current_row_idx == 0:
                return -1
            elif current_row_idx == len(menuItems)-1:
                return 0
            else:
                return menuItems[current_row_idx] + "/"
            

        print_menu(stdscr, current_row_idx, title, menuItems)
        stdscr.refresh()






