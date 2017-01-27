import os
import sys
from random import shuffle, random
from tkinter import *

buttons = []

SIDE = 6
QELEMENTS = SIDE ** 2 // 2

def cmd():
	print ("Button pressed")



main_window = Tk()

for i in range(SIDE):
	buttons.append([])
	for j in range(SIDE):
		b = Button (text = 'x',
					command = cmd)
		buttons[i].append(b)
		b.grid(row = i, column = j)

main_window.mainloop()