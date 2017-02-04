class Game(object):
	"""docstring for Game"""
	def __init__(self, side):
		print('Game config initialized')
		self.side = side
		self.qelements = side ** 2 // 2
		self.time = 0
		self.show_time = 3000 #in ms
		self.hide_time = 500 #in ms
		self.player_name = None
		self.images_opened = 0
		