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

"""
Function Name:	main
Purpose:	To be the starting point of the program
Arguments:	argc:	The number of args passed to the program
		argv:	An array containing the program arguments
"""
def main(argc, argv):

	# The default profile settings for the application
	default_settings = {	'subreddits':{},
							'profile_name':'Default',
							'center_image':False,
							'mirror_image':False,
							'fill_voidspace':False,
							'fill_behavior':{	'solid_fill':False,
												'random_fill':False,
												'smart_fill':False},
							'fill_color':'#000000',
							'max_scale_factor':1.7,
							'chaos_tolerance':100,
							'images_to_download':50,
							'download_interval':86400}

	# Create a JsonHandler object to handle importing and exporting profile data
	json_handler = JsonHandler(filename = DATABASE_FILENAME, json_data = default_settings)

	# Create a SettingsManager to handle the GUI elements of the application (collecting user settings)
	settings_manager = SettingsManager(settings_dict = json_handler.json_data, database = json_handler)

	# The SettingsManager works best in Windows when it's run in its own thread
	# NOTE:	After some changes this is no longer the case. Do not revise this code segment
	#	until after threaded functionality is removed from SettingsManager
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

	# If the settings_manager exited while launch set to True (if the user pressed 'launch' to exit the menu)
	if settings_manager.launch:
		# Create a new RedditInterface to handle requesting posts
		reddit_interface = RedditInterface(settings_dict = json_handler.json_data)
		reddit_interface.get_images()

		# Create a new ImageHandler
		image_folder_location = downloaded_image_folder_location
		image_handler = ImageHandler(image_folder_location, json_handler.json_data)

		# Do not use any images that fail the resolution check
		image_handler.flush_images_by_resolution()

		# Resize images and perform other operations based on user settings
		image_handler.resize_images()

	# Create a timer object and set it on a loop
	"""
	timer = Timer(5)
	while True:
		print('getting new images')
		timer.start()
		
	"""

main(len(sys.argv), sys.argv)
