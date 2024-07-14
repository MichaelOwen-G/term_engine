import curses
import os
import time

from engine.components.drawing import Drawing
from engine.components.drawing_stack import DrawingStack

# # width = 80
# # height = 60

# # # for i in range(4):
# # # 	print(i, end='\r')
# # # 	time.sleep(1)

# # # generate a 2d list from width amd height
# # screen_pixels_grid = []

# # for i in range(height):
# #   row = []
# #   for j in range(width):
# #     row.append("0")
# #   screen_pixels_grid.append(row)

# # screen1 = ''

# # for row in screen_pixels_grid:
# #   for p in row:
# #     screen1 = screen1 + p
# #   screen1 = screen1 + "\n"

# # screen = ''
# # for row in screen_pixels_grid:
# #   for p in row:
# #     screen = screen + "#"
# #   screen = screen + "\n"

# # os.system("cls")

# # while (True):
# # 	print(screen1, end="\r", flush = True)

# # 	print(screen, end='\r')


# x = 5
# y = 6
os.system('mode con: cols=94 lines=28')

stdscr = curses.initscr()
stdscr.clear()
stdscr.refresh()

def drawAt(x, y, str):
    stdscr.addstr(x, y, str)
    stdscr.refresh()

# frames = 0

# start = time.time()
# while (x < 25):
# 	stdscr.clear()
# 	drawAt(x, y, "#")
# 	x = x+1

# 	time.sleep(2)

# end= time.time()

# print(end - start)


# # stdscr.addstr(x, y, "this is a test string")
# # stdscr.refresh()

# # stdscr.addstr(0, 0, "##")

# # stdscr.refresh()

# # time.sleep(1)
# # # stdscr.getkey()

# # stdscr.addstr(x, y + 5, "this is a test string")
# # stdscr.refresh()


# # time.sleep(5)



wings =  Drawing("wings")
wings.drawFrames(
	[
    r'_/\_', "____",
    ], 
    stripNewLines=False,
)
print('WINGS', wings.frames)

body = Drawing("body")
body.draw(
'(____>',
stripNewLines=False
)
print("BODY", body.frames)


birdDrawing = DrawingStack()

print()

for dr in birdDrawing.stack:
    for f in dr.frames:
        #print(f)
        drawAt(0, 0, f[0])
        
time.sleep(5)        

# str = r'''
#  _/\_
# (____>
#  '''
# stripNewLines= True
# )

# stdscr.addstr(0, 16, "hello\nthere")
# stdscr.refresh()
# stdscr.addstr(0, 1, "world")
# stdscr.refresh()
# stdscr.addstr(10, 0, str)
# stdscr.refresh()
# time.sleep(5)