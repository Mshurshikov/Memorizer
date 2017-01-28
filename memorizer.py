import os
import sys
from random import shuffle, random
from tkinter import *

SIDE = 6
QELEMENTS = SIDE ** 2 // 2

buttons = []
numbers = []
main_window = Tk()

opened_images = 0
left_images = QELEMENTS

prev = None

def show(btns, nums, i, j):
	global prev
	global opened_images
	global left_images
	#btns[i][j].configure(text = nums[i*SIDE + j])
	btns[i][j].configure(image = images[i*SIDE + j])
	if prev:
		if (nums[prev[0]*SIDE + prev[1]] != nums[i*SIDE + j] 
			or ((btns[i][j].grid_info()['column'] == btns[prev[0]][prev[1]].grid_info()['column']) 
				and (btns[i][j].grid_info()['row'] == btns[prev[0]][prev[1]].grid_info()['row']))):
			main_window.after(1000, hide, btns, prev, i, j)
		else:
			progress_counter.configure(text = "Opened: " + str(opened_images + 1) + " Left: " + str(left_images - 1))
			opened_images += 1
			left_images -= 1
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
					relief=FLAT,
					command = lambda ii=i, jj=j:show(buttons,files,ii,jj))
		buttons[i].append(b)
		b.grid(row = i, column = j)

progress_counter = Label (text = "Opened: " + str(opened_images) + " Left: " + str(left_images))
progress_counter.grid(row = SIDE + 1, column = 0, columnspan = SIDE)

main_window.title("Memorizer")
main_window.after(2000, hide_all, buttons)
main_window.mainloop()