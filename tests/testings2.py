import curses
import curses.panel
import time

stdscr = curses.initscr()

stdscr.keypad(True)
 
curses.curs_set(0)  # Hide cursor
curses.noecho()  # Don't echo keystrokes

stdscr.nodelay(True)

panel = curses.newwin(10, 20, 10, 10)
panel2 = curses.newwin(20, 10, 0, 0)

panel.nodelay(True)

curses.panel.new_panel(panel)
curses.panel.new_panel(panel2)

panel.addstr(0,0, "Take a guess: ")
panel2.addstr(1, 1, "this is a test string")


panel.refresh()
panel2.refresh()

md = 'Hello world'

input = ''

while True:
    try:
        key_type = panel.getch()

        if key_type == ord(curses.KEY_UP):
            break   

        if key_type != -1:
            key = chr(key_type)

            if key_type == ord('ă'):
                break

            panel.addstr(0, 0, key)
            panel.refresh()
    except:
        pass


    # if key == ord('q'):
    #     break

    # convert the key int to character

    
    time.sleep(0.1)


    # if key == ord('q'):
    #     break

    # if key == ord('\n'):
    #     panel.addstr(0, 0, "Take a guess: ")

    # if key and key != ord('\n'):
    #     input += chr(key)

    




