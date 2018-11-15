from datetime import datetime, timedelta

class Timer:

	# Timer receives an interval in seconds
	def __init__(self, interval):
		self.now = None
		self.then = None
		self.interval = interval

	def start(self):
		self.now = datetime.now()
		self.then = self.now + timedelta(seconds = self.interval)

		while datetime.now() < self.then:
			pass

		return self.then
