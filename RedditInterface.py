import praw
import requests
import pathlib
from GlobalData import *
from FileHandler import *
from os import path


class RedditInterface:

	def __init__(self, settings_dict = None):

		self.settings_dict = settings_dict
		self.reddit = praw.Reddit(client_id = 'MUj_mV744SfYDg', client_secret = 'btDoplwBg9wrSZ1PWpMRiWTlgTw', user_agent = 'MatthewHarris481RDC')

	def clean_filename(self, filename):
	
		new_filename = ''
		for word in filename.split():
			new_filename = '{0}{1}'.format(new_filename, word)

		for x in range(len(new_filename)):
			if new_filename[x] == '\\':
				new_filename[x] = '_'

		return new_filename

	def get_images(self):
	
		dir_handler = DirectoryHandler(dirname = downloaded_image_folder_location)

		try:
			limit = self.settings_dict['images_to_download'] / (len(self.settings_dict['subreddits']) - 1)
		except ZeroDivisionError:
			return 0

		index = 0
		for sub in self.settings_dict['subreddits']:
			
			er = False
			try:
				submission_set = self.reddit.subreddit(sub).hot(limit = limit)
			except TypeError:
				er = True
				
			if er is False and sub != '':
				for submission in submission_set:
					image_path = path.join(downloaded_image_folder_location, self.clean_filename(submission.title))
					extension = pathlib.Path(submission.url).suffix
		
					if extension[1:] in valid_image_extensions:
						image_path = '{0}{1}'.format(image_path, extension)
						index += 1
						print('index: {0} sub: {1} url: {2}'.format(index, sub, image_path))
						with open(image_path, 'wb') as f:
							f.write(requests.get(submission.url).content)

		return index
