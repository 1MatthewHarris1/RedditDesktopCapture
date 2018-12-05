import sys
import ctypes
from os import listdir, makedirs, remove, getcwd
from os.path import isfile, join, basename, exists
from PIL import Image
from math import floor
from GlobalData import *
from webcolors import hex_to_rgb

# Get the screen resolution (depending on platform)
if sys.platform in supported_platforms:
	if sys.platform == 'darwin':
		from AppKit import NSScreen
		screen_width = NSScreen.mainScreen().frame().size.width
		screen_height = NSScreen.mainScreen().frame().size.height
	elif sys.platform == 'win32':
		from win32api import GetSystemMetrics
		screen_width = GetSystemMetrics(0)
		screen_height = GetSystemMetrics(1)


"""
Class Name:	ImageHandler
Responsibility:	To handle all operations of manipulating images
"""
class ImageHandler:

	image_filenames = []
	image_dictionary = {}
	image_folder_location = None
	invalid_image_directory = None
	wallpaper_image_directory = None
	new_image_list = []

	"""
	Function Name:	__init__
	Purpose:	Class Constructor
	Arguments:	image_folder_location:	The location of the image source folder
			settings_dict:	A dictionary of the user settings
	"""
	def __init__(self, image_folder_location, settings_dict):

		self.max_scale_factor = settings_dict['max_scale_factor']
		self.settings_dict = settings_dict
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.image_folder_location = image_folder_location
		self.invalid_image_directory = join(self.image_folder_location, 'InvalidImages')
		self.wallpaper_image_directory = join(self.image_folder_location, 'Wallpapers')
		self.get_directory_filenames()
		self.open_images()

	"""
	Function Name:	create_directory
	Purpose:	Create a new directory for the ImageDriver
	Arguments:	directory_name:	The name of the new directory to be created
	"""
	# NOTE: This should be replaced with the DirectoryHandler object
	@staticmethod
	def create_directory(directory_name):
		try:
			if not exists(directory_name):
				makedirs(directory_name)
		except OSError:
			print('Error creating directory "{0}"'.format(directory_name))

	"""
	Function Name:	is_valid_image_file
	Purpose:	Determine if the given file is a valid image file
	Arguments:	filename:	The name of the file to check
	"""
	@staticmethod
	def is_valid_image_file(filename):

		index = filename.rfind('.')
		valid_file_extensions = ['png', 'jpg', 'jpeg', 'tiff', 'bmp']
		if filename[index + 1:].lower() in valid_file_extensions:
			return filename[index:]
		else:
			return False

	@staticmethod
	def is_between(value, level, tolerance):
		lower = level - tolerance
		upper = level + tolerance
		if value >= lower and value <= upper:
			return True

		return False

	"""
	File Name:	get_directory_filenames
	Purpose:	Get all filenames in the given directory
	"""
	# NOTE: This should be replaced with the DirectoryHandler object
	def get_directory_filenames(self):

		directory = self.image_folder_location
		if exists(directory):
			for file in listdir(directory):
				if isfile(join(directory, file)):
					if self.is_valid_image_file(file):
						self.image_filenames.append(join(directory, file))
					else:
						print('"{0}" is not a valid image file'.format(file))
		else:
			print('The directory: "{0}" does not seem to exist'.format(directory))

	"""
	Function Name:	open_images
	Purpose:	Open all images in the image_filenames list
	"""
	def open_images(self):

		for filename in self.image_filenames:
			image = Image.open(filename)
			self.image_dictionary[filename] = image

	"""
	Function Name:	ge_minimum_scale_factor
	Purpose:	Ascertain the minimum scale factor required to resize the image to fit the screen
	Arguments:	image_resolution_tuple:	A tuple containing the screen width and height
	"""
	def get_minimum_scale_factor(self, image_resolution_tuple):
		width_div_factor = self.screen_width / image_resolution_tuple[0]
		height_div_factor = self.screen_height / image_resolution_tuple[1]
		min_scale_factor = min(width_div_factor, height_div_factor)

		return min_scale_factor

	"""
	Function Name:	mirror_and_center
	Purpose:	Mirror and center the given image
	Arguments:	image:	The image to mirror and center
			new_image_size:	The dimensions of the new image (to be created)
			color:	The color value to set the voidspace if the settings enable solid_fill
	"""
	def mirror_and_center(self, image, new_image_size, color = (0, 0, 0)):

		# Calculate size of voidspace
		voidspace_size = (self.screen_width - image.size[0], self.screen_height - image.size[1])

		# Create the new image in the appropriate color
		new_image = Image.new('RGB', new_image_size, color = color)

		# TODO: Redundant code here, try to optimize
		# Horizontal voidspace
		if voidspace_size[0] > voidspace_size[1]:
			margin_direction = 'h'
			margin_size = (voidspace_size[0] - image.size[0]) // 2
			if margin_size >= 0:
				image_position = (int((new_image_size[0] // 2)), int(voidspace_size[1]))
				new_image.paste(image, image_position)
				mirror_image = image.transpose(Image.FLIP_LEFT_RIGHT)
				new_image.paste(mirror_image, (int(margin_size), int(voidspace_size[1])))
				new_voidspace_size = margin_size
			else:
				image_position = (int(voidspace_size[0] // 2), int(voidspace_size[1]))
				new_image.paste(image, image_position)
				new_voidspace_size = int((new_image_size[0] - image.size[0]) // 2)
		# Vertical voidspace
		else:
			margin_direction = 'v'
			margin_size = int((int(voidspace_size[1]) - int(image.size[1])) // 2)
			if margin_size >= 0:
				image_position = (int(voidspace_size[0]), int((new_image_size[1] // 2)))
				new_image.paste(image, image_position)
				mirror_image = image.transpose(Image.FLIP_TOP_BOTTOM)
				new_image.paste(mirror_image, (int(voidspace_size[0]), int(margin_size)))
				new_voidspace_size = margin_size
			else:
				image_position = (int(voidspace_size[0]), int(voidspace_size[1] // 2))
				new_image.paste(image, image_position)
				new_voidspace_size = int((int(new_image_size[0]) - int(image.size[0])) // 2)

		return new_image, new_voidspace_size, margin_direction

	"""
	Function Name:	center
	Purpose:	Center the given image but do not mirror
	Arguments:	image:	The image to be centered
			new_image_size:	The size of the new image to be generated
			color:	The color of the voidspace is solid_fill is enabled in the profile settings
	"""
	def center(self, image, new_image_size, color = (0, 0, 0)):

		voidspace_size = ((int(int(self.screen_width) - int(image.size[0])) // 2), (int(int(self.screen_height) - int(image.size[1])) // 2))
		new_image = Image.new('RGB', new_image_size, color = color)

		image_position = (int(voidspace_size[0]), int(voidspace_size[1]))
		new_image.paste(image, image_position)

		return new_image

	"""
	Function Name:	put_margin_data
	Purpose:	Put data into the margins of an image
	"""
	def put_margin_data(self, image, start_index, margin_size, margin_direction, data):

		if margin_direction == 'h':

			image_coordinate = (start_index, 0)
			for y in range(margin_size):
				data[y].reverse()
				for x in range(y):
					print('puting pixel at {0}, {1} data: {2}'.format((x + image_coordinate[0]), y, data[y][x]))
					image.putpixel((x + image_coordinate[0], y), data[y][x])

		elif margin_direction == 'v':

			image_coordinate = (0, start_index)

		else:
			print('I got an invalid margin direction: "{0}"'.format(margin_direction))
			return None

		print('returning image')
		return image

	"""
	FunctionName:	get_margin_data
	Purpose:	Get data from the image margin
	"""
	def get_margin_data(self, image, start_index, margin_size, margin_direction):

		data_list = list(image.getdata())
		if margin_direction == 'h':

			operations = image.size[1]
			index_multiplier = image.size[0]

		elif margin_direction == 'v':

			operation = image.size[0]
			index_multiplier = image.size[1]

		else:
			print('I got an invalid margin direction: "{0}"'.format(margin_direction))
			return None

		color_list = []
		for num in range(operations):
			row_list = []
			data_index = (index_multiplier * num) + start_index
			for val in range(margin_size):
				row_list.append(data_list[data_index])
				data_index += 1
			color_list.append(row_list)

		return color_list

	"""
	Function Name:	resize_images
	Purpose:	Resize images according to resolution and perform actions specified by user settings
	"""
	def resize_images(self):

		new_image_size = (int(self.screen_width), int(self.screen_height))

		voidspace_color = (0, 0, 0)
		if self.settings_dict['fill_voidspace'] == 1:
			if self.settings_dict['fill_behavior']['solid_fill'] == 1:
				voidspace_color = hex_to_rgb(self.settings_dict['fill_color'])

		for entry in self.image_dictionary:
			image = self.image_dictionary[entry]

			if self.screen_width != image.size[0] and self.screen_height != image.size[1]:
				print('Resizing "{0}"'.format(entry))
				image_minimum_multiplication_factor = self.get_minimum_scale_factor(image.size)
				image_resize = (floor(image_minimum_multiplication_factor * image.size[0]), \
								floor(image_minimum_multiplication_factor * image.size[1]))

				image = image.resize(image_resize)
				if self.settings_dict['mirror_image'] == 1:
					new_image, voidspace_size, margin_direction = self.mirror_and_center(image, new_image_size, color = voidspace_color)
				elif self.settings_dict['center_image'] == 1:
					new_image = self.center(image, new_image_size, color = voidspace_color)
				else:
					new_image = image

				new_filename = str(len(self.new_image_list)) + self.is_valid_image_file(entry)
				new_filename = join(self.wallpaper_image_directory, new_filename)
				self.create_directory(self.wallpaper_image_directory)
				self.new_image_list.append(new_image)
				new_image.save(new_filename)

	"""
	Function Name:	flush_images_by_resolution
	Purpose:	Remove images that fail the resolution check
	"""
	def flush_images_by_resolution(self):

		slated_for_removal = []
		for entry in self.image_dictionary:
			scale_factor = self.get_minimum_scale_factor(self.image_dictionary[entry].size)
			output_str = '{0}:\t\t{1} x {2} | factor of {3}'
			output_str = \
				output_str.format(entry, self.image_dictionary[entry].size[0], self.image_dictionary[entry].size[1],
								  scale_factor)

			print(output_str)

			if scale_factor > self.max_scale_factor:
				new_file_location = join(self.invalid_image_directory, basename(entry))
				if isfile(entry):
					self.create_directory(self.invalid_image_directory)
					self.image_dictionary[entry].save(new_file_location)
					print('saved to: {0}'.format(new_file_location))
					try:
						self.image_dictionary[entry].close()
						slated_for_removal.append(entry)
					except Exception as exc:
						print(exc)
				else:
					print('could not find file: {0}'.format(entry))

		for entry in slated_for_removal:
			del self.image_dictionary[entry]
			remove(entry)
			print('removed: {0}'.format(entry))

