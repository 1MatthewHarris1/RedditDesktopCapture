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
	database_handler.print_all_tables()
	settings_manager = SettingsManager()
	settings_manager.start()
	settings_manager.join()

	"""
	timer = Timer(5)
	while True:
		print('getting new images')
		timer.start()
		
	"""

main(len(sys.argv), sys.argv)
