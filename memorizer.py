import os
import sys
import threading
import time
from random import shuffle, random
from tkinter import *
from tkinter import messagebox

SIDE = 6
QELEMENTS = SIDE ** 2 // 2

buttons = []
numbers = []
images = []

main_window = Tk()

images_opened = 0
images_left = QELEMENTS

time_left = 10

prev = None

def update_time_label():
	global time_left
	time_counter.configure(text = "Time left: " + str(time_left) + " seconds")
	time_left -= 1
	if time_left >= 0:
		main_window.after(1000, update_time_label)
	else:
		messagebox.showwarning("Game over", "Your time is up.")

def start_timer():
	print ('Starting...')
	global time_left
	time_left = 10
	update_time_label()
	print('Started')

def start_game(btns):
	global files, numbers, images
	files, numbers, images = initialize_game()
	for i in range(SIDE):
		for j in range(SIDE):
			btns[i][j].configure(image = images[i*SIDE + j], command = lambda ii=i, jj=j:show(buttons,files,ii,jj))
	main_window.after(2000, hide_all, buttons)

def show(btns, nums, i, j):
	global prev
	global images_opened
	global images_left
	#btns[i][j].configure(text = nums[i*SIDE + j])
	btns[i][j].configure(image = images[i*SIDE + j])
	if prev:
		if (nums[prev[0]*SIDE + prev[1]] != nums[i*SIDE + j] 
			or ((btns[i][j].grid_info()['column'] == btns[prev[0]][prev[1]].grid_info()['column']) 
				and (btns[i][j].grid_info()['row'] == btns[prev[0]][prev[1]].grid_info()['row']))):
			main_window.after(1000, hide, btns, prev, i, j)
		else:
			progress_counter.configure(text = "Opened: " + str(images_opened + 1) + " Left: " + str(images_left - 1))
			images_opened += 1
			images_left -= 1
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
	start_timer()

def initialize_game():

	nums = []
	imgs = []
	fls = os.listdir('gif')

	for i in range(1,100):
		nums.append(i)
	
	shuffle(nums)
	nums = nums[:QELEMENTS] * 2
	shuffle(nums)

	shuffle(fls)
	fls = fls[:QELEMENTS] * 2
	shuffle(fls)
	
	imgs = [PhotoImage(file = os.path.join('gif', image))for image in fls]

	return fls, nums, imgs

picQuestion = PhotoImage(file = 'FAQ.gif')

for i in range(SIDE):
	buttons.append([])
	for j in range(SIDE):
		b = Button (#text = numbers[i*SIDE + j],
					image = picQuestion,#images[i*SIDE + j],
					relief=FLAT
					)
		buttons[i].append(b)
		b.grid(row = i, column = j)

progress_counter = Label(text = "Opened: " + str(images_opened) + " Left: " + str(images_left))
progress_counter.grid(row = SIDE + 1, column = 0, columnspan = 2)

time_counter = Label(text = "Time left: " + str(time_left) + " seconds")
time_counter.grid(row = SIDE + 1, column = SIDE - SIDE//3, columnspan = 2)

start_button = Button(text = 'Start', command = lambda : start_game(buttons))
start_button.grid(row = SIDE + 1, column = SIDE//3, columnspan = 2)

main_window.title("Memorizer")


main_window.mainloop()