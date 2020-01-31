from magma import Catalan

class RS115(Catalan):
  """
  Permutations a1 a2 ... am-1 of [m-1] with longest decreasing subsequence of
    length at most 2 (no integers i < j < k such that ai > aj > ak)
  
  Data Type:
    tuple(int)
  Format:
    sequences of integers in the set [1,m-1]. [0] is considered the empty
    set, and [1] = {1}
  Generator:
    ()
  Example: (m=5)
    (3,1,2,4)
  """
  ID = 'RS115'
  names = ['321 Avoiding Permutations']
  keywords = {'permutations', 'sequence', 'avoiding', '321', 'three', 'two', 'one'}
  generator = lambda: ()
  
  @classmethod
  def product(cls, fst, snd):
    pass

  @classmethod
  def direct_norm(cls, permutation):
    return len(permutation) + 1