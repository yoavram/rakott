from datetime import datetime

def todaystr():
	"""Return the current day as a string, for example 20MAY2019 for May 20th, 2019.
	"""
	return datetime.now().strftime('%d%b%Y').upper()
