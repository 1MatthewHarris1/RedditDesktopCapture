#!/usr/bin/env python3

import sys
from SettingsManager import SettingsManager
from FileHandler import FileHandler
from DatabaseHandler import DatabaseHandler
from Timer import Timer
from GlobalData import *

def main(argc, argv):
	file_handler = FileHandler(DATABASE_FILENAME)

	construct_db = False
	if not file_handler.open_file():
		construct_db = True

	database_handler = DatabaseHandler(DATABASE_FILENAME, construct_db = construct_db)

	file_handler.close_file()


	settings_dict = {	'profile_name':database_handler.get_profile_attribute('profile_name'),
				'center_image':database_handler.get_profile_attribute('center_image'),
				'mirror_image':database_handler.get_profile_attribute('mirror_image'),
				'fill_voidapce':database_handler.get_profile_attribute('fill_voidspace'),
				'fill_behavior': {	'solid_fill':database_handler.get_profile_attribute('solid_fill'),
							'random_fill':database_handler.get_profile_attribute('random_fill'),
							'smart_fill':database_handler.get_profile_attribute('smart_fill')},
				'max_scale_factor':database_handler.get_profile_attribute('max_scale_factor'),
				'chaos_tolerance':database_handler.get_profile_attribute('chaos_tolerance'),
				'images_to_download':database_handler.get_profile_attribute('images_to_download'),
				'download_interval':database_handler.get_profile_attribute('download_interval')}

	settings_manager = SettingsManager(settings_dict = settings_dict)

	if sys.platform in supported_platforms:
		if sys.platform == 'darwin':
			settings_manager.run()
		else:
			settings_manager.start()
			settings_manager.join()

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
