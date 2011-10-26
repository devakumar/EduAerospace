dictionary = {'one':1,'two':2,'three':3}

class Test(object):
	def __init__(self):
		for key in dictionary.keys():
			self[key]=dictionary[key]

