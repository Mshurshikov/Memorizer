import os
import sys
import threading
import time
from random import shuffle, random
from tkinter import *
from tkinter import messagebox

class Game(object):
	"""docstring for Game"""

	side = 0
	#qelements = side ** 2 // 2
	images_opened = 0
	picQuestion = None
	numbers = []
	images = []
	time = 0

	def __init__(self, side, time):
		self.side = side
		self.qelements = side ** 2 // 2
		self.time = time

		self.numbers = self.generate_numbers(self.qelements)
		self.images = self.generate_images(self.qelements)

		self.picQuestion = PhotoImage(file = 'FAQ.gif')

		print('Game initialized')

	def generate_numbers(self, elements):
		numbers = []
		for i in range(1,100):
			numbers.append(i)
		shuffle(numbers)
		numbers = numbers[:elements] * 2
		shuffle(numbers)
		return numbers

	def generate_images(self, elements):
		files = os.listdir('gif')
		shuffle(files)
		files = files[:elements] * 2
		shuffle(files)
		images = [PhotoImage(file=os.path.join('gif', image)) for image in files]
		return images

class Control(object):
	"""docstring for Control"""
	
	buttons = []

	def __init__(self, buttons):
		self.buttons = buttons
	
	def start_game(self, numbers, images, side):
		#global files, numbers, images
		#files, numbers, images = initialize_game()
		for i in range(side):
			for j in range(side):
				self.buttons[i][j].configure(image = images[i*side + j], command = lambda ii=i, jj=j:show(buttons,files,ii,jj))
		main_window.after(2000, hide_all, buttons)

	def start_timer():
		print ('Starting...')
		global time_left
		time_left = 10
		update_time_label()
		print('Started')
	
	def show(btns, nums, i, j):
		print ('Button clicked')
		'''
		global prev
		global images_opened
		global images_left
		#btns[i][j].configure(text = nums[i*side + j])
		btns[i][j].configure(image = images[i*side + j])
		if prev:
			if (nums[prev[0]*side + prev[1]] != nums[i*side + j] 
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
		'''

	def hide(btns, prev, i, j):
		btns[i][j].configure(image = picQuestion)
		btns[prev[0]][prev[1]].configure(image = picQuestion)
	
	def hide_all(btns):
		'''
		for i in range(side):
			for j in range(side):
				btns[i][j].configure(image = picQuestion)
		start_timer()
		'''

	def update_time_label():
		'''
		global time_left
		time_counter.configure(text = "Time left: " + str(time_left) + " seconds")
		time_left -= 1
		if time_left >= 0:
			main_window.after(1000, update_time_label)
		else:
			messagebox.showwarning("Game over", "Your time is up.")					
		'''

class Picture(object):
	coordinates = ()
	"""docstring for Picture"""
	def __init__(self, coordinates):
		self.coordinates = coordinates

class Application(Frame):
	"""docstring for Application"""
	def __init__(self, master = None):
		Frame.__init__(self, master)
		self.grid()
		self.create_widgets()

	def create_widgets(self):
		self.progress_counter = Label(text = "Opened: 0 Left: 0")
		self.progress_counter.grid(row = 1, column = 0, columnspan = 1)

		self.time_counter = Label(text = "Time left: 0 seconds")
		self.time_counter.grid(row = 1, column = 1, columnspan = 1)

		#self.start_button = Button(text = 'Start', command = control.start_game(game.numbers, game.images, game.side))
		#self.start_button.grid(row = game.side + 1, column = game.side//3, columnspan = 2)
		
#main_window = Tk()

app = Application()
control = Control([])
game = Game(6, 10)
'''
for i in range(game.side):
	control.buttons.append([])
	for j in range(game.side):
		b = Button (#text = numbers[i*side + j],
					image = game.picQuestion,#images[i*side + j],
					relief=FLAT
					)
		control.buttons[i].append(b)
		b.grid(row = i, column = j)
'''

app.master.title("Memorizer")

app.mainloop()