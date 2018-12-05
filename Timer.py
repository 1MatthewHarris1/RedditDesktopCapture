from datetime import datetime, timedelta

"""
Class Name:	Timer
Responsibility:	Wait until the given number of seconds has elapsed
"""
class Timer:

	"""
	Function Name:	__init__
	Purpose:	Class Constructor
	Arguments:	interval:	The number of seconds for the timer to wait
	"""
	def __init__(self, interval):
		self.now = None
		self.then = None
		self.interval = interval

	"""
	Function Name:	start
	Purpose:	To start the timer
	"""
	def start(self):
		self.now = datetime.now()
		self.then = self.now + timedelta(seconds = self.interval)

		while datetime.now() < self.then:
			pass

		return self.then
