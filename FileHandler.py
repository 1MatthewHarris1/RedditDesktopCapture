from os import path, listdir, makedirs

class FileHandler:

	def __init__(self, filename, access_type = 'r'):

		self.filename = filename
		self.access_type = access_type
		self.file = None

	def open_existing_file(self):

			r = False
			if path.exists(self.filename) and path.isfile(self.filename):
				r = self.open_new_file()

			return r

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

	def close_file(self):

		if self.file is not None:
			self.file.close()

class DirectoryHandler:

	def __init__(self, dirname):

		self.dirname = dirname
		self.files = []

		if not path.exists(self.dirname):
			makedirs(self.dirname)

	def get_directory_filenames(self):

		if path.exists(self.dirname):
			for file in listdir(self.dirname):
				filename = path.join(self.dirname, file)
				if path.isfile(filename):
					self.files.append(FileHandler(filename))
