import json
from FileHandler import FileHandler
from GlobalData import DATABASE_FILENAME

class JsonHandler:

	def __init__(self, filename = None, json_data = None):

		self.json_data = json_data

		if filename is None:
			filename = DATABASE_FILENAME

		self.file_handler = FileHandler(filename)
		self.json_data = json_data

		if not self.file_handler.open_file():
			self.output_file_contents()

	def update_field_value(self, field, value):

		if field in self.json_data:
			self.json_data[field] = value

	def read_file_contents(self):

		if self.file_handler.open_file():
			self.json_data = json.load(self.file_handler.file)

			print(self.json_data)

	def output_file_contents(self):

		self.file_handler.file.write(json.dumps(self.json_data))
