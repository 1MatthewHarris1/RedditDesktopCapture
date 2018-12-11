from os import path, listdir, makedirs, remove

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
			# pass
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

if __name__ == '__main__':

	test_filename = 'test_file.txt'
	file_handler = FileHandler(test_filename, access_type = 'w')

	print('Attempted to open file "{0}" as existing file (should not exist)')
	if not file_handler.open_existing_file():
		print('Open failed (that\'s good!')
	else:
		print('Open succeeded... Ensure that file "{0}" does not exist and try again')
		print('Test Failed')
		exit(1)

	print('Attempting to open file "{0}" as new file')
	if file_handler.open_new_file():
		print('Open succeeded (that\'s good!')
		print('Attempting to remove test file')
		try:
			remove(test_filename)
		except:
			print('Removal failed...')
			print('Test failed')
			exit(1)
	else:
		print('Open failed...')
		print('Test failed')
		exit(1)

	print('Test succeeded')
	exit(0)



