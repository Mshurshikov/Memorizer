import os
import sys
from random import shuffle, random
from tkinter import *

SIDE = 6
QELEMENTS = SIDE ** 2 // 2

buttons = []
numbers = []
main_window = Tk()
picQuestion = PhotoImage(file = "FAQ.gif")

prev = None

def show(btns, nums, i, j):
	global prev
	btns[i][j].configure(text = nums[i*SIDE + j], image = '')
	if prev:
		if nums[prev[0]*SIDE + prev[1]] != nums[i*SIDE + j]:
			main_window.after(1000, hide, btns, prev, i, j)
		prev = None
	else:
		prev = (i,j)

def hide(btns, prev, i, j):
	btns[i][j].configure(image = picQuestion)
	btns[prev[0]][prev[1]].configure(image = picQuestion)

def hide_all(btns):
	for i in range(SIDE):
		for j in range(SIDE):
			btns[i][j].configure(image = picQuestion)

for i in range(1,100):
	numbers.append(i)

shuffle(numbers)
numbers = numbers[:QELEMENTS]
numbers = numbers * 2
shuffle(numbers)

for i in range(SIDE):
	buttons.append([])
	for j in range(SIDE):
		b = Button (text = numbers[i*SIDE + j],
					command = lambda ii=i, jj=j:show(buttons,numbers,ii,jj))
		buttons[i].append(b)
		b.grid(row = i, column = j)

main_window.title("Memorizer")
main_window.after(2000, hide_all, buttons)
main_window.mainloop()