from tkinter import Frame, Button, Entry, Tk, Checkbutton, Label, StringVar, IntVar, W as WEST, E as EAST
import threading

"""
As it uses Tkinter, SettingsManager runs
cleaner if it utilizes its own thread
"""
class SettingsManager(threading.Thread):

	def __init__(self, settings_dict = None, database = None):
		super().__init__()
		self.settings_dict = settings_dict
		self.database = database

	class Application(Frame):

		SUBFIELD_PADDING = 10
		DEFAULT_TEXT_ENTRY_WIDTH = 8

		class SubField:

			DISABLED = 'disabled'
			NORMAL = 'normal'
			
			def __init__(self, entry = None, button = None, text = ''):

				self.entry = entry
				self.button = button
				self.textvariable = text # StringVar(text)
				entry.textvariable = self.textvariable

		class CheckField:
		
			def __init__(self, master = None, text = None, state = 0, padding = 0):
				
				self.var = state # IntVar(state)
				self.padding = padding
				self.button = Checkbutton(master, text = text, variable = self.var, onvalue = 1, offvalue = 0)

		class TextField:

			def __init__(self, text = None, entry = None, label = None, padding = 0):

				self.var = "" # StringVar()
				self.padding = padding
				entry.textvariable = self.var # Entry(text = text, textvariable = self.var, width = 5)
				self.entry = entry
				self.entry.insert(0, text)
				self.label = label
				

		def __init__(self, parent = None, settings_dict = None, database = None):
			# always be sure to do this with tkinter child classes...
			super().__init__(parent)

			self.database = database
			self.settings_dict = settings_dict
			self.sub_list = []
			self.settings_list = []
			self.sub_label = None
			self.settings_label = None
			self.start_button = None
			self.save_profile_button = None
			self.quit_button = None

			self.initialize_widgets()

		def initialize_widgets(self):

			self.sub_label = Label(self, text = 'Subreddits', font = ('times', 18))
			self.settings_label = Label(self, text = 'Settings', font = ('times', 18))
			self.start_button = Button(self, text = 'Launch', command = self.start, font = ('times', 18))
			self.save_profile_button = Button(self, text = 'Save Profile', command = self.save_profile_data, font = ('times', 18))
			self.quit_button = Button(self, text = 'Exit', command = self.master.destroy, font = ('times', 18))
			self.add_sub_field()

			self.settings_dict_init(d = self.settings_dict)

		# Make this examine the various fields and correlate them to a specific type. Behave according to type
		def settings_dict_init(self, d = None, padding = 0):

			for element in d:
				if type(d[element]) is dict:
					self.settings_dict_init(d = d[element], padding = padding + self.SUBFIELD_PADDING)
				elif element in ['center_image', 'mirror_image', 'fill_voidspace', 'solid_fill', 'smart_fill', 'random_fill']:
					self.add_checkbutton(text = element, padding = padding)
				elif element in ['download_interval', 'profile_name', 'max_scale_factor', 'chaos_tolerance',
								 'images_to_download']:
					self.add_text_field(text = d[element], label_text = element, padding = padding)
				else:
					print('{0} has undefined behavior'.format(element))

			self.redraw()
			return

		def add_text_field(self, text = None, label_text = None, padding = 0):

			new_entry = Entry(self, width = self.DEFAULT_TEXT_ENTRY_WIDTH)
			new_label = Label(self, text = label_text)
			new_text_field = self.TextField(text = text, entry = new_entry, label = new_label)
			self.settings_list.append(new_text_field)

		def remove_sub_field(self, sub):

			if sub in self.sub_list:
				self.sub_list.remove(sub)
				sub.button.grid_forget()
				sub.entry.grid_forget()

			self.redraw()

			return

		# Consider a change to this paradigm. Fields should only go into the list after the '+' button is pressed
		def add_sub_field(self):

			new_button = Button(self, text = '+', command = self.add_sub_field, font = ('times', 11))
			new_text_entry = Entry(self)
			new_subfield = self.SubField(entry = new_text_entry, button = new_button)
			self.sub_list.append(new_subfield)

			self.redraw()

			return

		def add_checkbutton(self, text = None, padding = 0):

			new_checkbutton = self.CheckField(master = self, text = text, padding = padding)
			self.settings_list.append(new_checkbutton)

			return

		def redraw(self):

			# self.grid_forget()

			self.sub_label.grid(row = 0, column = 0, sticky = WEST, pady = 5)

			row = 1
			for x in range(len(self.sub_list)):
				subfield = self.sub_list[x]
				subfield.entry.grid(row = row, column = 0)
				subfield.button.grid(row = row, column = 1, sticky = WEST)
				if x < len(self.sub_list) - 1:
					subfield.button['command'] = lambda sub = subfield: self.remove_sub_field(sub)
					subfield.button['text'] = '-'
					subfield.entry['state'] = self.SubField.DISABLED
				row += 1

			row += 1
			self.settings_label.grid(row = row, column = 0, sticky = WEST, pady = 5)
			row += 1
			for x in range(len(self.settings_list)):
				
				if type(self.settings_list[x]) == self.CheckField:
					self.settings_list[x].button.grid(row = row, column = 0, sticky = WEST, padx = self.settings_list[x].padding)
				else:
					self.settings_list[x].entry.grid(row = row, column = 0, sticky = WEST, padx = self.settings_list[x].padding)
					self.settings_list[x].label.grid(row = row, column = 1, sticky = WEST, padx = self.settings_list[x].padding)

				row += 1
			
			self.quit_button.grid(row = row, column = 0, sticky = WEST, pady = 10)
			self.save_profile_button.grid(row = row, column = 1)
			self.start_button.grid(row = row, column = 2, sticky = EAST)

			self.grid()
			
			return

		def save_profile_data(self):

			subreddits = []
			for element in self.sub_list:
				subreddits.append(element.entry.textvariable)

			self.settings_dict['profile_name'] = str(self.settings_list[0].entry.get())
			self.settings_dict['center_image'] = self.settings_list[1].var
			self.settings_dict['mirror_image'] = self.settings_list[2].var
			self.settings_dict['fill_voidspace'] = self.settings_list[3].var
			self.settings_dict['fill_behavior']['solid_fill'] = self.settings_list[4].var
			self.settings_dict['fill_behavior']['random_fill'] = self.settings_list[5].var
			self.settings_dict['fill_behavior']['smart_fill'] = self.settings_list[6].var
			self.settings_dict['max_scale_factor'] = float(self.settings_list[7].entry.get())
			self.settings_dict['chaos_tolerance'] = int(self.settings_list[8].entry.get())
			self.settings_dict['images_to_download'] = int(self.settings_list[9].entry.get())
			self.settings_dict['download_interval'] = int(self.settings_list[10].entry.get())

			self.database.update_field_value('subreddits', subreddits)

			self.database.output_file_contents()

		def start(self):

			print('passing control to reddit image scraper module')

	def run(self):

		root = Tk()
		app = self.Application(root, settings_dict = self.settings_dict, database = self.database) # Instantiate the application class
		# app.grid()
		root.title("Reddit Desktop Capture")
		root.mainloop()
"""
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
