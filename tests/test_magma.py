import unittest
from magma import Catalan, Brackets, Mountain

class TestMagma(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    brackets = '{}{}{{{}{{{}}}}}'
    mountain = 'NNENNNEENEEENE'

    catalan_product = (((),()),())

    cls.test_objects = {Brackets: brackets, Mountain: mountain, Catalan: catalan_product}

  def test_identities(self):

    for Catalan_Family in (Catalan, Mountain, Brackets):
      self.assertEqual(Catalan_Family.identity()(self.test_objects[Catalan_Family]), self.test_objects[Catalan_Family])


