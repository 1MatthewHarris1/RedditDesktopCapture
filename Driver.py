#!/usr/bin/env python3

import sys
from SettingsManager import SettingsManager
from FileHandler import FileHandler
# from DatabaseHandler import DatabaseHandler
from RedditInterface import RedditInterface
from JsonHandler import JsonHandler
from Timer import Timer
from GlobalData import *
from ImageDriver import ImageHandler

def main(argc, argv):

	default_settings = {	'subreddits':{},
							'profile_name':'Default',
							'center_image':False,
							'mirror_image':False,
							'fill_voidspace':False,
							'fill_behavior':{	'solid_fill':False,
												'random_fill':False,
												'smart_fill':False},
							'max_scale_factor':1.7,
							'chaos_tolerance':100,
							'images_to_download':50,
							'download_interval':86400}

	json_handler = JsonHandler(filename = DATABASE_FILENAME, json_data = default_settings)

	settings_manager = SettingsManager(settings_dict = json_handler.json_data, database = json_handler)


	if sys.platform in supported_platforms:
		if sys.platform == 'darwin':
			settings_manager.run()
		elif sys.platform == 'win32':
			# settings_manager.start()
			# settings_manager.join()
			settings_manager.run()
		else:
			print('Unknown platform. Exiting...')
			sys.exit(1)

	if settings_manager.launch:
		reddit_interface = RedditInterface(settings_dict = json_handler.json_data)
		reddit_interface.get_images()

		image_folder_location = downloaded_image_folder_location
		image_handler = ImageHandler(image_folder_location, json_handler.json_data)
		image_handler.flush_images_by_resolution()
		image_handler.resize_images()

	"""
	timer = Timer(5)
	while True:
		print('getting new images')
		timer.start()
		
	"""

main(len(sys.argv), sys.argv)
