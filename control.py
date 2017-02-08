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

		self.update_time = 1000
		self._timer = None
		
		
		#init views
		self.login = view.Login(master)
		self.game = view.Game(master)
		self.score = view.Score(master)

		#init closing routine
		self.login.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.game.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.score.protocol("WM_DELETE_WINDOW", self.on_closing)

		self.new_game()

	def init_login(self):
		self.login.player_name_input.delete(0, 'end')
		self.login.start_game_button.configure(command = self.start_game)

	def init_game(self):
		self.game.create_labels(self.game_config.side, self.game_config.qelements)
		self.buttons = self.game.create_buttons(self.game_config.side)
		for i in range(self.game_config.side):
			for j in range(self.game_config.side):
				self.buttons[i][j].configure(command = lambda row = i, column = j: self.check_pictures(row, column))

		self.game.stop_button.configure(command = self.stop_game)

		self.game.images,self.files = self.generate_images(self.game_config.qelements)
		self.game.show_all(self.buttons, self.game_config.side)
		self.game.after(self.game_config.show_time, self.game.hide_all, self.buttons, self.game_config.side)
		self.game.after(self.game_config.show_time, self.start_timer)

	def init_score(self):
		self.score.new_game_button.configure(command = self.new_game)

	def new_game(self):
		self.buttons = []
		self.previous_picture = ()
		self.game_config = model.Game(side = 6)
		self.game.withdraw()
		self.score.withdraw()
		self.login.deiconify()
		self.init_login()

	def start_game(self):
		if self.login.player_name_input.get():
			self.game_config.player_name = self.login.player_name_input.get()
			print('Game started')
			self.login.withdraw()
			self.game.deiconify()
			self.init_game()
		else:
			messagebox.showwarning("Enter player", "Please, enter your name to begin.")

	def stop_game(self):
		self.stop_timer()
		self.game.show_all(self.buttons, self.game_config.side)
		self.game.withdraw()
		self.score.deiconify()
		self.init_score()
		self.score.show_results((self.game_config.player_name, self.game_config.score, self.game_config.time))
		print ('Game stopped')
		print ('Game score: {0}, Time: {1}, Pictures found: {2} from {3}'.format(self.game_config.score, self.game_config.time, self.game_config.images_opened, self.game_config.qelements))

	def start_timer(self):
		self.game.time_counter.configure(text = "Time: " + str(self.game_config.time) + " seconds")
		self.game_config.time += 1
		self._timer = self.game.after(self.update_time, self.start_timer)

	def stop_timer(self):
		if self._timer:
			print ('Timer stopped')
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
				self.game_config.score += self.game_config.success
			else:
				self.game.after(self.game_config.hide_time, self.game.hide, self.buttons, self.previous_picture, row, column)
				self.game_config.score -= self.game_config.failure
			self.previous_picture = None
			self.game.score_counter.configure(text = "Score: {0}".format(self.game_config.score))
		else:
			self.previous_picture = (row, column)

		if self.game_config.images_opened == self.game_config.qelements:
			self.stop_game()
			messagebox.showinfo('Congratulations', 'Congratulations, {0}! \nYou found all pictures. \nGame score: {1}, Time: {2}, Pictures found: {3} from {4}'.format(self.game_config.player_name, self.game_config.score, self.game_config.time, self.game_config.images_opened, self.game_config.qelements))
