import tkinter as tk
import view as view
import model as model

class Controller(object):
	"""docstring for Controller"""
	def __init__(self, master):
		print('Root initialized')
		#init models
		self.game_config = model.Game(side = 6)
		
		#init views
		self.login = view.Login(master)
		self.game = view.Game(master)
		self.score = view.Score(master)

		self.game.withdraw()
		self.score.withdraw()

		self.init_login()

	def init_login(self):
		self.login.start_game_button.configure(command = self.start_game)

	def init_game(self):
		self.buttons = self.game.create_buttons(self.game_config.side)
		self.game.create_labels(self.game_config.side, self.game_config.qelements)

	def start_game(self):
		print('Game started')
		self.login.withdraw()
		self.game.deiconify()
		self.init_game()