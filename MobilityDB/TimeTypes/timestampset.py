from datetime import datetime, timedelta
from bdateutil.parser import parse
from .period import Period
import warnings

try:
	# Do not make psycopg2 a requirement.
	from psycopg2.extensions import ISQLQuote
except ImportError:
	warnings.warn('psycopg2 not installed', ImportWarning)


class TimestampSet:
	"""
	Set of disjoint timestamp values
	"""
	__slots__ = ['_datetimeList']

	def __init__(self, *argv):
		# Constructor with a single argument of type string
		self._datetimeList = []
		if len(argv) == 1 and isinstance(argv[0], str):
			ts = argv[0].strip()
			if ts[0] == '{' and ts[-1] == '}':
				ts = ts[1:-1]
				times = ts.split(",")
				for time in times:
					self._datetimeList.append(parse(time.strip()))
			else:
				raise Exception("ERROR: Could not parse timestamp set value")
		# Constructor with a single argument of type list
		elif len(argv) == 1 and isinstance(argv[0], list):
			# List of strings representing datetime values
			if all(isinstance(arg, str) for arg in argv[0]):
				for arg in argv[0]:
					self._datetimeList.append(parse(arg))
			# List of datetimes
			elif all(isinstance(arg, datetime) for arg in argv[0]):
				for arg in argv[0]:
					self._datetimeList.append(arg)
			else:
				raise Exception("ERROR: Could not parse timestamp set value")
		# Constructor with multiple arguments
		else:
			# Arguments are of type string
			if all(isinstance(arg, str) for arg in argv):
				for arg in argv:
					self._datetimeList.append(parse(arg))
			# Arguments are of type datetime
			elif all(isinstance(arg, datetime) for arg in argv):
				for arg in argv:
					self._datetimeList.append(arg)
			else:
				raise Exception("ERROR: Could not parse timestamp set value")
		# Verify validity of the resulting instance
		self._valid()

	def _valid(self):
		if any(x >= y for x, y in zip(self._datetimeList, self._datetimeList[1:])):
			raise Exception("ERROR: The timestamps of a timestamp set must be increasing")

	def timespan(self):
		"""
		Interval
		"""
		return self._datetimeList[-1] - self._datetimeList[0]

	def period(self):
		"""
		Period on which the timestamp set is defined ignoring the potential time gaps
		"""
		return Period(self._datetimeList[0], self._datetimeList[-1], True, True)

	def numTimestamps(self):
		"""
		Number of distinct timestamps
		"""
		return len(self._datetimeList)

	def startTimestamp(self):
		"""
		Start timestamp
		"""
		return self._datetimeList[0]

	def endTimestamp(self):
		"""
		End timestamp
		"""
		return self._datetimeList[-1]

	def timestampN(self, n):
		"""
		N-th distinct timestamp
		"""
		# 1-based
		if 0 < n <= len(self._datetimeList):
			return self._datetimeList[n - 1]
		else:
			raise Exception("ERROR: there is no value at this index")

	def timestamps(self):
		"""
		Distinct timestamps
		"""
		return self._datetimeList

	def shift(self, timedelta):
		"""
		Shift
		"""
		return TimestampSet([datetime + timedelta for datetime in self._datetimeList])

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			if (len(other._datetimeList) == len(self._datetimeList) and
				set(other._datetimeList).intersection(self._datetimeList)):
				return True
		return False

	# Psycopg2 interface.
	def __conform__(self, protocol):
		if protocol is ISQLQuote:
			return self

	def getquoted(self):
		return "{}".format(self.__str__())
	# End Psycopg2 interface.

	@staticmethod
	def read_from_cursor(value, cursor=None):
		if not value:
			return None
		return TimestampSet(value)

	def __str__(self):
		return "'{{{}}}'".format(', '.join('{}'.format(datetime.__str__())
			for datetime in self._datetimeList))

	def __repr__(self):
		return (f'{self.__class__.__name__ }'
				f'({self._datetimeList!r})')