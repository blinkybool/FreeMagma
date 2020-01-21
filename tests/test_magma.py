import unittest
from magma import Catalan, Brackets, Mountains

class TestMagma(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    brackets = '{}{}{{{}{{{}}}}}'
    mountain = '\n'.join(
                        [r'     /\       ',
                         r'    /  \/\    ',
                         r' /\/      \   ',
                         r'/          \/' + '\\']) # can't end raw-string literal in a backslash

    catalan_product = (((),()),())

    cls.test_objects = {Brackets: brackets, Mountains: mountain, Catalan: catalan_product}

  def test_identities(self):

    for Catalan_Family in (Catalan, Mountains, Brackets):
      self.assertEqual(Catalan_Family.identity()(self.test_objects[Catalan_Family]), self.test_objects[Catalan_Family])


