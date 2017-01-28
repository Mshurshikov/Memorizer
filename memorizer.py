import os
import sys
from random import shuffle, random
from tkinter import *

SIDE = 6
QELEMENTS = SIDE ** 2 // 2

buttons = []
numbers = []
main_window = Tk()


prev = None

def show(btns, nums, i, j):
	global prev
	#btns[i][j].configure(text = nums[i*SIDE + j])
	btns[i][j].configure(image = images[i*SIDE + j])
	#print(btns[prev[0]][prev[1]].grid_info())
	#print(btns[i][j].grid_info())
	if prev:
		coordinates = btns[i][j].grid_info()
		prev_coordinates = btns[prev[0]][prev[1]].grid_info()
		if (nums[prev[0]*SIDE + prev[1]] != nums[i*SIDE + j] 
			or ((coordinates['column'] == prev_coordinates['column']) and (coordinates['row'] == prev_coordinates['row']))):
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
numbers = numbers[:QELEMENTS] * 2
shuffle(numbers)

files = os.listdir('gif')
shuffle(files)
files = files[:QELEMENTS] * 2
shuffle(files)

picQuestion = PhotoImage(file = 'FAQ.gif')
images = [PhotoImage(file = os.path.join('gif', image))for image in files]

for i in range(SIDE):
	buttons.append([])
	for j in range(SIDE):
		b = Button (text = numbers[i*SIDE + j],
					image = images[i*SIDE + j],
					command = lambda ii=i, jj=j:show(buttons,files,ii,jj))
		buttons[i].append(b)
		b.grid(row = i, column = j)

main_window.title("Memorizer")
main_window.after(2000, hide_all, buttons)
main_window.mainloop()