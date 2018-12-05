from os import path, listdir, makedirs

"""
Class Name:	FileHandler
Responsibility:	Handle file I/O operations while performing exception handling
"""
class FileHandler:

	"""
	Function Name:	__init__
	Purpose:	Class Constructor
	Arguments:	filename:	The name of the file to access
			access_type:	The access type for the file
	"""
	def __init__(self, filename, access_type = 'r'):

		self.filename = filename
		self.access_type = access_type
		self.file = None

	"""
	Function Name:	open_existing_file
	Purpose:	Only open the specified file if it already exists
	"""
	def open_existing_file(self):

			r = False
			if path.exists(self.filename) and path.isfile(self.filename):
				r = self.open_new_file()

			return r

	"""
	Function Name:	open_new_file
	Purpose:	Open the specified file no matter what (if possible)
	"""
	def open_new_file(self):

		r = False
		try:
			self.file = open(self.filename, self.access_type)
			r = True
		except IOError as e:
			print("IOError({0}): {1}".format(e.errno, e.strerror))
		except Exception as e:
			print("Unknown Error in FileHandler")
		
		return r

	"""
	Function Name:	close_file
	Purpose:	Close the specified file
	"""
	def close_file(self):

		if self.file is not None:
			self.file.close()

"""
Class Name:	DirectoryHandler
Responsibility:	Handle directory operations
"""
class DirectoryHandler:

	"""
	Function Name:	__init__
	Purpose:	Class constructor
	"""
	def __init__(self, dirname):

		self.dirname = dirname
		self.files = []

		if not path.exists(self.dirname):
			makedirs(self.dirname)

	"""
	Function Name:	get_directory_filenames
	Purpose:	Get the filenames of every file in a particular directory
	"""
	def get_directory_filenames(self):

		if path.exists(self.dirname):
			for file in listdir(self.dirname):
				filename = path.join(self.dirname, file)
				if path.isfile(filename):
					self.files.append(FileHandler(filename))
