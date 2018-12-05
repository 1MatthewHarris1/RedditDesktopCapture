import praw
import requests
import pathlib
from GlobalData import *
from FileHandler import *
from os import path


"""
Class Name:	RedditInterface
Responsibility:	To handle all Reddit operations such as finding new images
"""
class RedditInterface:

	"""
	Function Name:	__init__
	Purpose:	Class constructor
	Arguments:	settings_dict:	A dictionary of the user settings
	"""
	def __init__(self, settings_dict = None):

		self.settings_dict = settings_dict
		self.reddit = praw.Reddit(client_id = 'MUj_mV744SfYDg', client_secret = 'btDoplwBg9wrSZ1PWpMRiWTlgTw', user_agent = 'MatthewHarris481RDC')

	"""
	Function Name:	clean_filename
	Purpose:	'Sanitize' the specified filename into a string of characters usable for a system filename
	Arguments:	filename:	The name of the file to be sanitized
	"""
	def clean_filename(self, filename):
	
		new_filename = ''
		# Remove whitespace
		for word in filename.split():
			new_filename = '{0}{1}'.format(new_filename, word)

		# Remove '\' characters
		for x in range(len(new_filename)):
			if new_filename[x] == '\\':
				new_filename[x] = '_'

		return new_filename

	"""
	Function Name:	get_images
	Purpose:	To get new images from Reddit based on the user's input subreddits and image download number
	"""
	def get_images(self):
	
		# Create a new DirectoryHandler for hanlding directory operations
		dir_handler = DirectoryHandler(dirname = downloaded_image_folder_location)

		# Try to divide the number of subreddits equally (fails when 0 subreddits listed)
		try:
			limit = self.settings_dict['images_to_download'] / (len(self.settings_dict['subreddits']) - 1)
		except ZeroDivisionError:
			return 0

		index = 0

		# For each subreddit specified by the user
		for sub in self.settings_dict['subreddits']:
			
			# Try to collect some images
			er = False
			try:
				submission_set = self.reddit.subreddit(sub).hot(limit = limit)
			except TypeError:
				er = True
				
			# If there were no errors
			if er is False and sub != '':

				# For each submission
				for submission in submission_set:

					# Create a new path for the image
					image_path = path.join(downloaded_image_folder_location, self.clean_filename(submission.title))

					# Retain the image extension
					extension = pathlib.Path(submission.url).suffix
		
					# If the extension is valid
					if extension[1:] in valid_image_extensions:

						# Complete the image path
						image_path = '{0}{1}'.format(image_path, extension)
						index += 1
						print('index: {0} sub: {1} url: {2}'.format(index, sub, image_path))

						# Open and write the image to a file
						with open(image_path, 'wb') as f:
							f.write(requests.get(submission.url).content)

		return index
