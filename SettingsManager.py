from tkinter import Frame, Button, Tk
import threading

"""
As it uses Tkinter, SettingsManager runs
cleaner if it utilizes its own thread
"""
class SettingsManager(threading.Thread):

	def __init__(self):
		super().__init__()

	class Application(Frame):

		def __init__(self, parent=None, height = 50, width = 50):
			# always be sure to do this with tkinter child classes...
			super().__init__(parent)
			quitButton = Button(self, text="Goodbye, World!",
								command=self.quit,
								font=('times', 24))
			quitButton.grid()

	def run(self):

		print('Application window should open...')
		root = Tk()
		app = self.Application(root) # Instantiate the application class
		app.grid() # "grid" is a Tkinter geometry manager
		root.title("Sample Application")
		root.mainloop() # Wait for events, until "quit()" method is called
		print("done")
