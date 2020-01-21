import unittest
from magma import Brackets, Mountains

class TestBrackets(unittest.TestCase):

  def test_identity(self):
    brackets = '{}{}{{{}{{{}}}}}'
    self.assertEqual(Brackets.identity()(brackets), brackets)

class TestMountains(unittest.TestCase):

  def test_identity(self):
    mountain = '\n'.join(
                        [r'     /\       ',
                         r'    /  \/\    ',
                         r' /\/      \   ',
                         r'/          \/' + '\\']) # can't end raw-string literal in a backslash
    self.assertEqual(Mountains.identity()(mountain), mountain)