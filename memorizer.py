import os
import sys
import threading
import time
from random import shuffle, random
from tkinter import *
from tkinter import messagebox

class Control(object):
	"""docstring for Control"""

	NEXT = 0
	SUCCESS = 1
	FAILURE = 2

	def __init__(self, side, time):
		self.qelements = side ** 2 // 2
		self.time = time

		self.images_opened = 0

		self.numbers = self.generate_numbers(self.qelements)
		self.images, self.files = self.generate_images(self.qelements)

		self.prev_picture = Picture()
	
	def start_game(self, side, buttons):
		for i in range(side):
			for j in range(side):
				buttons[i][j].configure(image = self.images[i*side + j])
	
	def check_pictures(self, buttons, side, row, column):
		buttons[row][column].configure(image = self.images[row*side + column])	
		if self.prev_picture.coordinates:
			if ((self.files[self.prev_picture.coordinates[0]*side + self.prev_picture.coordinates[1]] == self.files[row*side + column])
				and ((row,column) != (self.prev_picture.coordinates[0], self.prev_picture.coordinates[1]))):
				self.images_opened += 1
				self.prev_picture.coordinates = None
				return self.SUCCESS
			else:
				return self.FAILURE
		else:
			self.prev_picture.coordinates = (row,column)
			return self.NEXT

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
		return images, files

class Picture(object):
	"""docstring for Picture"""
	def __init__(self):
		self.coordinates = ()

class Application(Frame):
	"""docstring for Application"""
	def __init__(self, side, master = None):
		Frame.__init__(self, master)
		self.pic_question = PhotoImage(file = 'FAQ.gif')
		self.side = side
		self.controller = Control(side, time = 120)
		self.grid()
		self.buttons = self.create_buttons()
		self.create_labels()

	def create_buttons(self):
		buttons = []
		for i in range(self.side):
			buttons.append([])
			for j in range(self.side):
				b = Button (image = self.pic_question,
							command = lambda row = i, column = j: self.picture_click(row,column),
							relief=FLAT
							)
				buttons[i].append(b)
				b.grid(row = i, column = j)
		return buttons

	def create_labels(self):
		self.progress_counter = Label(text = "Opened: 0 Left: 0")
		self.progress_counter.grid(row = self.side + 1, column = 0, columnspan = self.side // 3)

		self.start_button = Button(text = 'Start', command = self.start_click)
		self.start_button.grid(row = self.side + 1, column = self.side // 3, columnspan = self.side // 3)

		self.time_counter = Label(text = 'Time left: ' + str(self.controller.time) + ' seconds')
		self.time_counter.grid(row = self.side + 1, column = self.side - (self.side // 3), columnspan = self.side // 3)

	def start_click(self):
		self.controller.start_game(self.side, self.buttons)
		self.after(2000, self.hide_all)
		self.after(2000, self.update_time_label)
		print ('Start game')

	def picture_click(self, row, column):
		check = self.controller.check_pictures(self.buttons, self.side, row, column)
		if check == self.controller.SUCCESS:
			self.progress_counter.configure(text = "Opened: " + str(self.controller.images_opened) + " Left: " + str(self.controller.qelements - self.controller.images_opened))
		elif check == self.controller.FAILURE:
			self.after(1000, self.hide, row, column)

	def update_time_label(self):
		self.time_counter.configure(text = "Time left: " + str(self.controller.time) + " seconds")
		self.controller.time -= 1
		if self.controller.time >= 0:
			self.after(1000, self.update_time_label)
		else:
			messagebox.showwarning("Game over", "Your time is up.")	
	
	def hide(self, row, column):
		self.buttons[row][column].configure(image = self.pic_question)
		self.buttons[self.controller.prev_picture.coordinates[0]][self.controller.prev_picture.coordinates[1]].configure(image = self.pic_question)
		self.controller.prev_picture.coordinates = None
	
	def hide_all(self):
		for i in range(self.side):
			for j in range(self.side):
				self.buttons[i][j].configure(image = self.pic_question)	

app = Application(side = 6)
#control = Control(app.side, 10)

app.master.title("Memorizer")

app.mainloop()