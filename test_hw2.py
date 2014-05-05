import hw2
import random
import unittest

class Test(unittest.TestCase):
  def test_simple_example(self):
    example = {'Alice': ('0', '1', '2', '3'), 'Bob': ('1', '2'),
        'Charlie': ('2', '3'), 'Denise': ('3', '0')}
    correct_result = {'0': ('Alice', 'Denise'), '1': ('Alice', 'Bob'),
        '2': ('Bob', 'Charlie'), '3': ('Charlie', 'Denise')}
    result = hw2.Solve(example)
    for slot in '0123':
      self.assertIn(slot, result)
      self.assertEqual(correct_result[slot], tuple(sorted(result[slot])))
