import unittest
from app.eurusd.py import Eurusd

class EurusdTdd(unittest.TestCase):

	def setUp(self):
		self.eurusd = Eurusd()

	def test(self):
		result = self.eurusd.
