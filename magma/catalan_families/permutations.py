from magma import Catalan

class RS115(Catalan):
  """
  Permutations a1 a2 ... an-1 of [n-1] with longest decreasing subsequence of
    length at most 2 (no integers i<j<k such that ai > aj > ak)
  Data Type: tuple(int)
  Format: length n-1 permutations of the set of positive integers [1,n-1]
  Generator: ()
  Example: (n=5) (3,1,2,4)
  """
  RS = 115
  names = ['321 Avoiding Permutations']
  keywords = {'permutations', 'sequence', 'avoiding', '321'}
  generator = lambda: ()
  
  @classmethod
  def product(cls, fst, snd):
    pass