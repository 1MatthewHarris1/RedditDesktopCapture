import sqlite3

database_schema = """
CREATE TABLE Subreddits
(
	subreddit	text UNIQUE
);
CREATE TABLE ProfileInfo
(
	profile_name	TEXT DEFAULT 'Default',
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
);
INSERT INTO ProfileInfo DEFAULT VALUES
"""

class DatabaseHandler:

	def __init__(self, filename, construct_db = False):

		self.__database = sqlite3.connect(filename)
		self.__cursor = self.__database.cursor()
		if construct_db is True:
			self.construct_database()

	def print_all_tables(self):

		for row in self.__database.execute("SELECT * FROM sqlite_master WHERE type='table';"):
			self.__print_table(str(row[1]))

	def __print_table(self, table_name):

		display = "{}: ".format(table_name)
		print(display)

		col_names = [row[1] for row in self.__cursor.execute("PRAGMA table_info({})".format(table_name))]
		print(col_names)

		rows = self.__cursor.execute("SELECT * FROM {}".format(table_name))
		for row in rows:
			print(row)
		print()

	def construct_database(self):

		self.__cursor.executescript(database_schema)

	def add_subreddit(self, subreddit_name):

		sql_query = '''
		INSERT INTO Subreddits(subreddit)
		Values({0})
		'''.format(subreddit_name)
		self.__cursor.execute(sql_query)

	def get_subreddit_list(self):

		sql_query = '''
		SELECT *
		FROM Subreddits
		'''

		sub_list = []
		for row in self.__cursor.execute(sql_query):
			sub_list.append(row[0])

		return sub_list

	def get_profile_attribute(self, attr_name):

		sql_query = '''
		SELECT {0}
		FROM ProfileInfo
		'''.format(attr_name)

		attr_list = []
		for row in self.__cursor.execute(sql_query):
			attr_list.append(row[0])

		return attr_list

	def set_profile_attrivute(self, attr_name, value):

		sql_query = '''
		UPDATE ProfileInfo
		SET {0} = '{1}'
		'''.format(attr_name, value)

		self.__cursor.execute(sql_query)
