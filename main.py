import tkinter as tk
from control import Controller

if __name__ == '__main__':
	root = tk.Tk()
	root.title('Memorizer')
	Controller(root)
	root.withdraw()
	root.mainloop()
