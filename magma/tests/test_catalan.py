import unittest
from magma import Catalan

class TestCatalan(unittest.TestCase):

  MAX_NORM = 8

  def test_identities(self):

    catalan_families = list(Catalan.all_catalan_families())

    for Catalan_Family in catalan_families:
      identity = Catalan_Family.identity()
      for m in range(1,self.MAX_NORM+1):
        for obj in Catalan_Family.products(m):
          self.assertEqual(identity(obj), obj)