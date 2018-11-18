from tkinter import Frame, Button, Entry, Tk
import threading

"""
As it uses Tkinter, SettingsManager runs
cleaner if it utilizes its own thread
"""
class SettingsManager(threading.Thread):

	def __init__(self):
		super().__init__()


	class Application(Frame):

		class SubField:
			
			def __init__(self, entry = None, button = None, text = ''):

				self.entry = entry
				self.button = button
				self.textvariable = text
				entry.textvariable = self.textvariable

		def __init__(self, parent=None):
			# always be sure to do this with tkinter child classes...
			super().__init__(parent)
			self.sub_list = []
			self.initialize_widgets()

		def initialize_widgets(self):

			self.add_text_field()

		def remove_text_field(self):
			pass

		def add_text_field(self):

			self.grid_forget()
			new_button = Button(self, text = '+', command = self.add_text_field, font = ('times', 11))
			new_text_entry = Entry(self)
			new_subfield = self.SubField(entry = new_text_entry, button = new_button)
			self.sub_list.append(new_subfield)

			row = 0
			for x in range(len(self.sub_list)):

				subfield = self.sub_list[x]
				subfield.entry.grid(row = row, column = 0)
				subfield.button.grid(row = row, column = 1)
				if x < len(self.sub_list) - 1:
					subfield.button.command = self.remove_text_field
					subfield.button.text = '-'
					row += 1

			return
			
				

	def run(self):

		print('Application window should open...')
		root = Tk()
		app = self.Application(root) # Instantiate the application class
		app.grid() # "grid" is a Tkinter geometry manager
		root.title("Sample Application")
		root.mainloop() # Wait for events, until "quit()" method is called
		print("done")


"""
CREATE TABLE Subreddits
(
	subreddit	text UNIQUE
);
CREATE TABLE ProfileInfo
(
	profile_name	TEXT DEFAULT 'Default',
	center_image	INT DEFAULT 0,
	mirror_image	INT DEFAULT 0,
	fill_voidspace	INT DEFAULT 0,
	solid_fill		INT DEFAULT 0,
	random_fill		INT DEFAULT 0,
	smart_fill		INT DEFAULT 0,
	max_scale_factor	REAL DEFAULT 1.7,
	chaos_tolerance		INT DEFAULT 100,
	images_to_download	INT DEFAULT 50,
	download_interval	INT DEFAULT 86400
);
INSERT INTO ProfileInfo DEFAULT VALUES
"""
