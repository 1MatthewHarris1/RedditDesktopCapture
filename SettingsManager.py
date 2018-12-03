from tkinter import Frame, Button, Entry, Tk, Checkbutton, Label, StringVar, IntVar, W as WEST
import threading

"""
As it uses Tkinter, SettingsManager runs
cleaner if it utilizes its own thread
"""
class SettingsManager(threading.Thread):

	def __init__(self, settings_dict = None):
		super().__init__()
		self.settings_dict = settings_dict


	class Application(Frame):

		SUBFIELD_PADDING = 10

		class SubField:

			DISABLED = 'disabled'
			NORMAL = 'normal'
			
			def __init__(self, entry = None, button = None, text = ''):

				self.entry = entry
				self.button = button
				self.textvariable = StringVar(text)
				entry.textvariable = self.textvariable

		class CheckField:
		
			def __init__(self, text = None, state = 0, padding = 0):
				
				self.var = IntVar(state)
				self.padding = padding
				self.checkbutton = Checkbutton(text = text, variable = self.var, onvalue = 1, offvalue = 0)
				

		def __init__(self, parent = None, settings_dict = None):
			# always be sure to do this with tkinter child classes...
			super().__init__(parent)
			self.settings_dict = settings_dict
			self.sub_list = []
			self.check_list = []
			self.sub_label = None
			self.settings_label = None
			self.initialize_widgets()

		def initialize_widgets(self):

			self.sub_label = Label(self, text = 'Subreddits', font = ('times', 18))
			self.settings_label = Label(self, text = 'Settings', font = ('times', 18))
			self.add_text_field()

			self.dict_checkbutton_init(d = self.settings_dict)

		def dict_checkbutton_init(self, d = None, padding = 0):

			for element in d:
				if type(d[element]) is dict:
					self.dict_checkbutton_init(d = d[element], padding = padding + self.SUBFIELD_PADDING)
				else:
					self.add_checkbutton(text = element, padding = padding)

			return

		"""
		def enable_button(self, button):
			
			print('button enabled')
			button['state'] = SettingsManager.Subfield.NORMAL
		"""

		def remove_text_field(self, sub):

			if sub in self.sub_list:
				self.sub_list.remove(sub)

			self.redraw()

			return

		def add_text_field(self):

			new_button = Button(self, text = '+', command = self.add_text_field, font = ('times', 11))
			new_text_entry = Entry(self)
			new_subfield = self.SubField(entry = new_text_entry, button = new_button)
			self.sub_list.append(new_subfield)

			self.redraw()

			return

		def add_checkbutton(self, text = None, padding = 0):

			new_checkbutton = self.CheckField(text = text, padding = padding)
			self.check_list.append(new_checkbutton)

			self.redraw()

			return

		def redraw(self):

			# self.grid_forget()
			self.sub_label.grid(row = 0, column = 0)
			row = 1
			for x in range(len(self.sub_list)):
				subfield = self.sub_list[x]
				subfield.entry.grid(row = row, column = 0)
				subfield.button.grid(row = row, column = 1)
				if x < len(self.sub_list) - 1:
					subfield.button['command'] = lambda sub = subfield: self.remove_text_field(sub)
					subfield.button['text'] = '-'
					subfield.entry['state'] = self.SubField.DISABLED
				row += 1
				"""
				else:
					subfield.button['state'] = self.SubField.DISABLED
				"""
			row += 2
			self.settings_label.grid(row = row, column = 0)
			row += 1
			for x in range(len(self.check_list)):
				self.check_list[x].checkbutton.grid(row = row, column = 0, sticky = WEST, padx = self.check_list[x].padding)
				row += 1

			self.grid()
			
			return

	def run(self):

		root = Tk()
		app = self.Application(root, settings_dict = self.settings_dict) # Instantiate the application class
		# app.grid()
		root.title("Reddit Desktop Capture")
		root.mainloop()


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
