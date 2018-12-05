"""
import sys
from SettingsManager import SettingsManager
from GlobalData import *

def main(argc, argv):
	pass

main(len(sys.argv), sys.argv)
"""

import sys
import ctypes
from os import listdir, makedirs, remove, getcwd
from os.path import isfile, join, basename, exists
from PIL import Image
from win32api import GetSystemMetrics
from math import floor
from GlobalData import *
# from SkinTones import skin_tones, skin_tone_tolerance


class ImageHandler:
	MAX_SCALE_FACTOR = 1.7
	image_filenames = []
	image_dictionary = {}
	image_folder_location = None
	invalid_image_directory = None
	wallpaper_image_directory = None
	screen_width = GetSystemMetrics(0)
	screen_height = GetSystemMetrics(1)
	new_image_list = []

	def __init__(self, image_folder_location):
		self.image_folder_location = image_folder_location
		self.invalid_image_directory = join(self.image_folder_location, 'InvalidImages')
		self.wallpaper_image_directory = join(self.image_folder_location, 'Wallpapers')
		self.get_directory_filenames()
		self.open_images()

	@staticmethod
	def create_directory(directory_name):
		try:
			if not exists(directory_name):
				makedirs(directory_name)
		except OSError:
			print('Error creating directory "{0}"'.format(directory_name))

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

	def open_images(self):

		for filename in self.image_filenames:
			image = Image.open(filename)
			self.image_dictionary[filename] = image

	def get_minimum_scale_factor(self, image_resolution_tuple):
		width_div_factor = self.screen_width / image_resolution_tuple[0]
		height_div_factor = self.screen_height / image_resolution_tuple[1]
		min_scale_factor = min(width_div_factor, height_div_factor)

		return min_scale_factor

	def mirror_and_center(self, image, new_image_size):

		voidspace_size = (self.screen_width - image.size[0], self.screen_height - image.size[1])
		new_image = Image.new('RGB', new_image_size)

		color = (0, 0, 0)
		if voidspace_size[0] > voidspace_size[1]:
			margin_direction = 'h'
			margin_size = (voidspace_size[0] - image.size[0]) // 2
			if margin_size >= 0:
				image_position = ((new_image_size[0] // 2), voidspace_size[1])
				new_image.paste(image, image_position)
				mirror_image = image.transpose(Image.FLIP_LEFT_RIGHT)
				new_image.paste(mirror_image, (margin_size, voidspace_size[1]))
				new_voidspace_size = margin_size
			else:
				image_position = ((voidspace_size[0] // 2), voidspace_size[1])
				new_image.paste(image, image_position)
				new_voidspace_size = (new_image_size[0] - image.size[0]) // 2
		else:
			margin_direction = 'v'
			margin_size = (voidspace_size[1] - image.size[1]) // 2
			if margin_size >= 0:
				image_position = (voidspace_size[0], (new_image_size[1] // 2))
				new_image.paste(image, image_position)
				mirror_image = image.transpose(Image.FLIP_TOP_BOTTOM)
				new_image.paste(mirror_image, (voidspace_size[0], margin_size))
				new_voidspace_size = margin_size
			else:
				image_position = (voidspace_size[0], (voidspace_size[1] // 2))
				new_image.paste(image, image_position)
				new_voidspace_size = (new_image_size[0] - image.size[0]) // 2

		return new_image, new_voidspace_size, margin_direction

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

	def resize_images(self):

		"""
		def is_skin_color(color):

			color_is_skin_color = False
			for tone in skin_tones:
				tone_is_skin_color = True
				for x in range(3):
					if not self.is_between(color[x], tone[x], skin_tone_tolerance[x]):
						tone_is_skin_color = False
				if tone_is_skin_color:
					color_is_skin_color = True
					break

			return color_is_skin_color
		"""

		new_image_size = (self.screen_width, self.screen_height)

		for entry in self.image_dictionary:
			image = self.image_dictionary[entry]

			if self.screen_width != image.size[0] and self.screen_height != image.size[1]:
				print('Resizing "{0}"'.format(entry))
				image_minimum_multiplication_factor = self.get_minimum_scale_factor(image.size)
				image_resize = (floor(image_minimum_multiplication_factor * image.size[0]), \
								floor(image_minimum_multiplication_factor * image.size[1]))

				image = image.resize(image_resize)
				new_image, voidspace_size, margin_direction = self.mirror_and_center(image, new_image_size)

				"""
				margin_1_data = self.get_margin_data(image, 0, voidspace_size, margin_direction)
				margin_2_data = self.get_margin_data(image, voidspace_size, voidspace_size, margin_direction)

				new_image = self.put_margin_data(new_image, voidspace_size, voidspace_size, margin_direction, margin_1_data)
				new_image = self.put_margin_data(new_image, voidspace_size + image.size[0], voidspace_size, margin_direction, margin_2_data)
				"""

				new_filename = str(len(self.new_image_list)) + self.is_valid_image_file(entry)
				new_filename = join(self.wallpaper_image_directory, new_filename)
				self.create_directory(self.wallpaper_image_directory)
				self.new_image_list.append(new_image)
				new_image.save(new_filename)

	"""
	def relocate_originals(self):

		slated_for_removal = []
		for entry in self.image_dictionary:
			if isfile(entry):
				self.create_directory(self.original_image_directory)
				new_file_location = join(self.original_image_directory, basename(entry))
				try:
					self.image_dictionary[entry].save(new_file_location)
					print('saved to: {0}'.format(new_file_location))
				except Exception as exc:
					print(exc, '{0}'.format(new_file_location))

				try:
					self.image_dictionary[entry].close()
					slated_for_removal.append(entry)
				except Exception as exc:
					print(exc, '{0}'.format(entry))

		for entry in slated_for_removal:
			del self.image_dictionary[entry]
			remove(entry)
			print('removed: {0}'.format(entry))
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

			if scale_factor > self.MAX_SCALE_FACTOR:
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

		"""
	def run(self):

		# image_folder_location = getcwd()
		# image_folder_location = input('Image Folder Location: ')
		image_folder_location = downloaded_image_folder_location # 'C:/Users/Matthew/Desktop/RDC'
		image_handler = ImageHandler(image_folder_location)
		image_handler.flush_images_by_resolution()
		image_handler.resize_images()
		# image_handler.relocate_originals()
		# sys.exit(0)
		"""
