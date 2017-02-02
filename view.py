import tkinter as tk
from tkinter import messagebox

class Login(tk.Toplevel):
	"""docstring for Login"""
	def __init__(self, master):
		print('Login initialized')
		tk.Toplevel.__init__(self, master)
		self.title('Login')

		self.grid()
		self.player_name_label = tk.Label(self, text = 'Player:')
		self.player_name_label.grid(row = 0, column = 0)
		
		self.player_name_input = tk.Entry(self)
		self.player_name_input.grid(row = 0, column = 1)

		self.start_game_button = tk.Button(self, text = 'Start')
		self.start_game_button.grid(row = 1, column = 1)


class Game(tk.Toplevel):
	"""docstring for Game"""
	def __init__(self, master):
		print('Game initialized')
		tk.Toplevel.__init__(self, master)
		self.title('Memorizer')
		
		self.pic_question = tk.PhotoImage(file = 'FAQ.gif')
		
		self.images = None

		self.grid()

	def create_labels(self, side, qelements):
		self.progress_counter = tk.Label(self, text = "Opened: 0 Left: " + str(qelements))
		self.progress_counter.grid(row = side + 1, column = 0, columnspan = side // 3)

		self.start_button = tk.Button(self, text = 'Stop')
		self.start_button.grid(row = side + 1, column = side // 3, columnspan = side // 3)

		self.time_counter = tk.Label(self, text = 'Time: 0 seconds')
		self.time_counter.grid(row = side + 1, column = side - (side // 3), columnspan = side // 3)

	def create_buttons(self, side):
		buttons = []
		for i in range(side):
			buttons.append([])
			for j in range(side):
				b = tk.Button (self, 
							image = self.pic_question,
							relief = tk.FLAT)
				buttons[i].append(b)
				b.grid(row = i, column = j)
		return buttons

	def hide_all(self, buttons, side):
		for i in range(side):
			for j in range(side):
				buttons[i][j].configure(image = self.pic_question)

	def show_all(self, buttons, side):
		for i in range(side):
			for j in range(side):
				buttons[i][j].configure(image = self.images[i*side + j])

class Score(tk.Toplevel):
	"""docstring for Score"""
	def __init__(self, master):
		print('Score initialized')
		tk.Toplevel.__init__(self, master)
		self.title('Score')