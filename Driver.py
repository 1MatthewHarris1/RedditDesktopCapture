#!/usr/bin/env python3

import sys
from SettingsManager import SettingsManager
from FileHandler import FileHandler
from DatabaseHandler import DatabaseHandler
from JsonHandler import JsonHandler
from Timer import Timer
from GlobalData import *

def main(argc, argv):
	file_handler = FileHandler(DATABASE_FILENAME)

	construct_db = False
	if not file_handler.open_file():
		construct_db = True

	database_handler = DatabaseHandler(DATABASE_FILENAME, construct_db = construct_db)

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

	# file_handler.close_file()

	"""
	settings_dict = {	'profile_name':('text', database_handler.get_profile_attribute('profile_name')),
				'center_image':('checkbutton', database_handler.get_profile_attribute('center_image')),
				'mirror_image':('checkbutton',database_handler.get_profile_attribute('mirror_image')),
				'fill_voidapce':('checkbutton', database_handler.get_profile_attribute('fill_voidspace')),
				'fill_behavior': {	'solid_fill':('checkbutton', database_handler.get_profile_attribute('solid_fill')),
							'random_fill':('checkbutton', database_handler.get_profile_attribute('random_fill')),
							'smart_fill':('checkbutton', database_handler.get_profile_attribute('smart_fill'))},
				'max_scale_factor':('number', database_handler.get_profile_attribute('max_scale_factor')),
				'chaos_tolerance':('number', database_handler.get_profile_attribute('chaos_tolerance')),
				'images_to_download':('number', database_handler.get_profile_attribute('images_to_download')),
				'download_interval':('number', database_handler.get_profile_attribute('download_interval'))}
	"""

	settings_manager = SettingsManager(settings_dict = json_handler.json_data, database = json_handler)

	if sys.platform in supported_platforms:
		if sys.platform == 'darwin':
			settings_manager.run()
		elif sys.platform == 'win32':
			settings_manager.start()
			settings_manager.join()
		else:
			print('Unknown platform. Exiting...')
			sys.exit(1)

	"""
	database_handler.print_all_tables()
	print('profile:', database_handler.get_profile_attribute('profile_name'))
	print('center image:', database_handler.get_profile_attribute('center_image'))
	print('mirror image:', database_handler.get_profile_attribute('mirror_image'))
	print('images to download: ', database_handler.get_profile_attribute('images_to_download'))
	"""

	"""
	timer = Timer(5)
	while True:
		print('getting new images')
		timer.start()
		
	"""

"""
	profile_name	TEXT DEFAULT 'Default'
	center_image	INT DEFAULT 0,
	mirror_image	INT DEFAULT 0,
	fill_voidspace	INT DEFAULT 0,
	solid_fill		INT DEFAULT 0,
	random_fill		INT DEFAULT 0,
	smart_fill		INT DEFAULT 0,
	max_scale_factor	REAL DEFAULT 1.7,
	chaos_tolerance		INT DEFAULT 100,
	images_to_download	INT DEFAULT 50,
	download_interval	INT DEFAULT 86400
"""

main(len(sys.argv), sys.argv)
