import json
from FileHandler import FileHandler
from GlobalData import DATABASE_FILENAME

"""
Class Name:	JsonHandler
Responsibility:	Handle operations for importing and exporting JSON data to file
"""
class JsonHandler:

	"""
	Function Name:	__init__
	Purpose:	Class constructor
	Arguments:	filename:	The filename of the .json file
			json_data:	a dict object with data to be serialized into JSON
	"""
	def __init__(self, filename = None, json_data = None):

		self.json_data = json_data

		# filename defaults to DATABASE_FILENAME
		if filename is None:
			filename = DATABASE_FILENAME

		self.filename = filename

		# Create a FileHandler object for hanlding file I/O
		self.file_handler = FileHandler(filename, access_type = 'r')

		# If this file does not already exist
		if not self.file_handler.open_new_file():

			# Accept the data passed in rather than reading from the file
			self.json_data = json_data

			# Output the json_data to the file
			self.output_file_contents()
		else:
			
			# Read the JSON data from the file
			self.read_file_contents()

	"""
	Function Name:	update_field_value
	Purpose:	Update the value of the specified field
	Arguments:	field:	the key of the field value in the json_data dict
			value:	the value to set for the dict field
	"""
	def update_field_value(self, field, value):

		# Ensure that the field is in the dictionary before adding
		if field in self.json_data:
			self.json_data[field] = value

	"""
	Function Name:	set_file_handler_access_type
	Purpose:	Reset the FileHandler access type depending on the input parameter
	Arguments:	access_type:	The new access type of the FileHandler
	"""
	def set_file_handler_access_type(self, access_type):

		if self.file_handler is not None:
			self.file_handler.close_file()
		self.file_handler = FileHandler(self.filename, access_type = access_type)
		if not self.file_handler.open_new_file():
			self.file_handler.open_existing_file()

	"""
	Function Name:	read_file_contents
	Purpose:	Read the contents of the JSON file
	"""
	def read_file_contents(self):

		self.set_file_handler_access_type('r')
		if self.file_handler.open_existing_file():
			self.json_data = json.load(self.file_handler.file)

	"""
	Function Name:	output_file_contents
	Purpose:	Output the contents of the file into JSON
	"""
	def output_file_contents(self):

		self.set_file_handler_access_type('wb')
		self.file_handler.file.write(bytes(json.dumps(self.json_data), 'utf-8'))
		self.file_handler.close_file()
