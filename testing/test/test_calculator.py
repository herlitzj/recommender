import unittest
from app.calculator import Calculator

class TddInPythonExample(unittest.TestCase):

	def setUp(self):
		self.calc = Calculator()

	def test_calculator_add_method_returns_correct_result(self):
		result = self.calc.add(2,2)
		self.assertEqual(4, result)

	def test_calculator_returns_error_message_if_both_entries_are_not_numbers(self):
		self.assertRaises(ValueError, self.calc.add, 'two', 'three')
		self.assertRaises(TypeError, self.calc.sub, 'two', 'three')

	def test_calculator_returns_error_message_if_first_entry_is_not_number(self):
		self.assertRaises(ValueError, self.calc.add, 'two', 3)

	def test_calculator_returns_error_message_if_second_entry_is_not_number(self):
		self.assertRaises(ValueError, self.calc.add, 2, 'three')

	def test_calculator_subtract_method_returns_correct_result(self):
		result = self.calc.sub(4,7)
		self.assertEqual(-3,result)

	def test_calculator_multipy_method_returns_correct_result(self):
		result = self.calc.mult(2,3)
		self.assertEqual(6,result)

	def test_calculator_divide_method_returns_correct_result(self):
		result = self.calc.div(8,2)
		self.assertEqual(4,result)

	def test_calculator_factorial_method_returns_correct_result(self):
		result = self.calc.fact(5)
		self.assertEqual(120, result)
