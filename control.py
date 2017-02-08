import os
from random import shuffle

import tkinter as tk
from tkinter import messagebox

import view as view
import model as model

class Controller(object):
	"""docstring for Controller"""
	def __init__(self, master):
		print('Root initialized')
		self.master = master
		self.buttons = []
		self.previous_picture = ()
		self.update_time = 1000
		#init models
		self.game_config = model.Game(side = 6)
		
		#init views
		self.login = view.Login(master)
		self.game = view.Game(master)
		self.score = view.Score(master)

		#init closing routine
		self.login.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.game.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.score.protocol("WM_DELETE_WINDOW", self.on_closing)

		self.game.withdraw()
		self.score.withdraw()

		self.init_login()

	def init_login(self):
		self.login.start_game_button.configure(command = self.start_game)

	def init_game(self):
		self.game.create_labels(self.game_config.side, self.game_config.qelements)
		self.buttons = self.game.create_buttons(self.game_config.side)
		for i in range(self.game_config.side):
			for j in range(self.game_config.side):
				self.buttons[i][j].configure(command = lambda row = i, column = j: self.check_pictures(row, column))

		self.game.images,self.files = self.generate_images(self.game_config.qelements)
		self.game.show_all(self.buttons, self.game_config.side)
		self.game.after(self.game_config.show_time, self.game.hide_all, self.buttons, self.game_config.side)
		self.game.after(self.game_config.show_time, self.start_timer)

	def start_game(self):
		if self.login.player_name_input.get():
			self.game_config.player_name = self.login.player_name_input.get()
			print('Game started')
			self.login.withdraw()
			self.game.deiconify()
			self.init_game()
		else:
			messagebox.showwarning("Enter player", "Please, enter your name to begin.")

	def start_timer(self):
		self.game.time_counter.configure(text = "Time: " + str(self.game_config.time) + " seconds")
		self.game_config.time += 1
		self._timer = self.game.after(self.update_time, self.start_timer)

	def stop_timer(self):
		print ('Timer stopped')
		if self._timer:
			self.game.after_cancel(self._timer)
			self._timer = None

	def on_closing(self):
		print('Closing...')
		self.stop_timer()
		self.master.destroy()

	def generate_images(self, elements):
		files = os.listdir('gif')
		shuffle(files)
		files = files[:elements] * 2
		shuffle(files)
		images = [tk.PhotoImage(file=os.path.join('gif', image)) for image in files]
		return images, files

	def check_pictures(self, row, column):
		self.buttons[row][column].configure(image = self.game.images[row*self.game_config.side + column])
		if self.previous_picture:
			if ((self.files[self.previous_picture[0]*self.game_config.side + self.previous_picture[1]] == self.files[row*self.game_config.side + column])
				and ((row,column) != (self.previous_picture[0], self.previous_picture[1]))):
				self.game_config.images_opened += 1
				self.game.progress_counter.configure(text = "Opened: " + str(self.game_config.images_opened) + " Left: " + str(self.game_config.qelements - self.game_config.images_opened))
				self.buttons[row][column].configure(state="disabled")
				self.buttons[self.previous_picture[0]][self.previous_picture[1]].configure(state="disabled")
			else:
				self.game.after(self.game_config.hide_time, self.game.hide, self.buttons, self.previous_picture, row, column)
			self.previous_picture = None
		else:
			self.previous_picture = (row, column)
