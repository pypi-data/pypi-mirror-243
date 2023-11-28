import random
import string


def get_all_subclasses(cls):
    '''Returns all subclasses of a given base class'''
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses

def none_or_greater_than(a, b):
	'''returns True if a is greater than b or None'''
	if a:
		return a > b
	else:
		return True

def none_or_less_than(a, b):
	'''returns True if a is less than b or None'''
	if a:
		return a < b
	else:
		return True

def id_generator(size=6, chars=string.ascii_uppercase):
	'''generates random strings of specified lenght within known ranges'''
	return ''.join(random.choice(chars) for _ in range(size))

def first(iterable, default = None):
  '''Just resturns the first item of an iterable. With default.'''
  iterator = iter(iterable)
  return next(iterator, default)