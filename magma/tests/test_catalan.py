import unittest
from magma import Catalan, MatchingBrackets, RS25 as Mountains

class TestCatalan(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    brackets = '()()((()((()))))'
    mountain = 'UUDUUUDDUDDDUD'
    catalan_product = (((),()),())

    cls.test_objects = {MatchingBrackets: brackets, Mountains: mountain, Catalan: catalan_product}

  def test_identities(self):

    for Catalan_Family in (Catalan, Mountains, MatchingBrackets):
      self.assertEqual(Catalan_Family.identity()(self.test_objects[Catalan_Family]), self.test_objects[Catalan_Family])