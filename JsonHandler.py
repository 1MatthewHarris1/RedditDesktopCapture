import json
from FileHandler import FileHandler
from GlobalData import DATABASE_FILENAME

class JsonHandler:

	def __init__(self, filename = None, json_data = None):

		self.json_data = json_data

		if filename is None:
			filename = DATABASE_FILENAME

		self.filename = filename

		self.file_handler = FileHandler(filename, access_type = 'r')
		if not self.file_handler.open_new_file():
			self.json_data = json_data
			self.output_file_contents()
		else:
			self.read_file_contents()

	def update_field_value(self, field, value):

		if field in self.json_data:
			self.json_data[field] = value

	def set_file_handler_access_type(self, access_type):

		if self.file_handler is not None:
			self.file_handler.close_file()
		self.file_handler = FileHandler(self.filename, access_type = access_type)
		if not self.file_handler.open_new_file():
			self.file_handler.open_existing_file()

	def read_file_contents(self):

		self.set_file_handler_access_type('r')
		if self.file_handler.open_existing_file():
			self.json_data = json.load(self.file_handler.file)

	def output_file_contents(self):

		self.set_file_handler_access_type('wb')
		self.file_handler.file.write(bytes(json.dumps(self.json_data), 'utf-8'))
		self.file_handler.close_file()
