import praw
import requests
import pathlib
from GlobalData import *
from os import path

reddit = praw.Reddit(client_id = 'MUj_mV744SfYDg', client_secret = 'btDoplwBg9wrSZ1PWpMRiWTlgTw', user_agent = 'MatthewHarris481RDC')

def clean_filename(filename):

	new_filename = ''
	for word in filename.split():
		new_filename = '{0}{1}'.format(new_filename, word)

	return new_filename

for submission in reddit.subreddit('earthporn').hot(limit = 10):
	image_path = path.join(downloaded_image_folder_location, clean_filename(submission.title))
	extension = pathlib.Path(submission.url).suffix

	if extension[1:] in valid_image_extensions:
		image_path = '{0}{1}'.format(image_path, extension)
		print(image_path)
		with open(image_path, 'wb') as f:
			f.write(requests.get(submission.url).content)
