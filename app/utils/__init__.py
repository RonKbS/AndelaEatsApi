from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta, datetime

db = SQLAlchemy()


def to_camel_case(snake_str):
	"""Format string to camel case."""
	title_str = snake_str.title().replace("_", "")
	return title_str[0].lower() + title_str[1:]


def to_pascal_case(word, sep='_'):
	return ''.join(list(map(lambda x: x.capitalize(), word.split(sep))))


def daterange(date1, date2):
	for n in range(int((date2 - date1).days)+1):
		yield date1 + timedelta(n)


def current_time_by_zone(zone):
	# zone format: +1 or -3
	
	current_date = None
	if zone[0:1] == '+':
		current_date = datetime.utcnow() + timedelta(hours=int(zone[1:]))
	else:
		current_date = datetime.utcnow() - timedelta(hours=int(zone[1:]))
	
	return current_date
