import os
import sys
import threading
import time
from random import shuffle, random
from tkinter import *

SIDE = 6
QELEMENTS = SIDE ** 2 // 2

buttons = []
numbers = []
main_window = Tk()

images_opened = 0
images_left = QELEMENTS

time_left = 10

prev = None

def timer():
	
	while 1:
		time_left -= 1
		update_time_label(time_left)
		time.sleep(1)

def update_time_label():
	global time_left
	time_counter.configure(text = "Time left: " + str(time_left) + " seconds")
	time_left -= 1
	if time_left >= 0:
		main_window.after(1000, update_time_label)
	else:
		print('Game over')

def start_timer():
	print ('Starting...')
	update_time_label()
	print('Started')

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

progress_counter = Label(text = "Opened: " + str(images_opened) + " Left: " + str(images_left))
progress_counter.grid(row = SIDE + 1, column = 0, columnspan = SIDE//2)

time_counter = Label(text = "Time left: " + str(time_left) + " seconds")
time_counter.grid(row = SIDE + 1, column = SIDE//2, columnspan = SIDE//2)

#t = threading.Timer(1, timer)

main_window.title("Memorizer")
main_window.after(2000, hide_all, buttons)


main_window.mainloop()