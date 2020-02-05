from magma import Catalan

def rothe_diagram(permutation):
  if len(permutation)==0:
    return '+'
  perm_indices = range(1, len(permutation)+1)
  rows = ((' * ' if permutation[i-1]==j else '   ' for j in perm_indices) for i in perm_indices)

  line_sep = '+---' * len(permutation) + '+'

  rothe_diagram = (line_sep 
                    + '\n'
                    + ('\n' + line_sep + '\n').join('|' + '|'.join(row) + '|' for row in rows)
                    + '\n'
                    + line_sep)

  return rothe_diagram

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
  keywords = {'permutation', 'sequence', 'avoiding', '321', 'three', 'two', 'one'}

  generator = lambda: ()
  
  @classmethod
  def product(cls, fst, snd):
    new_snd = [None] + list(snd)

    last_white = 0
    for i, snd_i in enumerate(snd, start=1):
      if snd_i > i:
        new_snd[last_white] = snd_i
        last_white = i
  
    new_snd[last_white] = len(snd) + 1

    return fst + tuple(x + len(fst) for x in new_snd)

  @classmethod
  def factorise(cls, perm):
    # recognise right multiplication by generator
    if perm[-1] == len(perm):
      return (perm[:-1], ())
    
    # convert perm to list to shift the white dots
    # add dumby item at index 0 to make shift_perm[i] the same as perm_i
    shift_perm = [None] + list(perm)

    # index of the rightmost white dot (above the diagonal)
    white_index = shift_perm.index(len(perm))

    # undo the cascading of white dots from the right until one passes the diagonal
    for i in reversed(range(1,white_index)):
      # test if there is a white dot here
      if shift_perm[i] > i:
        # shift the last white dot to this column as long as it doesn't pass
        # the diagonal
        if shift_perm[i] >= white_index:
          shift_perm[white_index] = shift_perm[i]
          white_index = i
        else:
          # this dot is the extra dot added by the product function
          break
    
    # slice up to the critical white dot (-1 to account for different indexing)
    fst = perm[:white_index-1]
    snd = tuple(x-white_index+1 for x in shift_perm[white_index+1:])
    
    return (fst, snd)

  @classmethod
  def direct_norm(cls, permutation):
    return len(permutation) + 1

  @classmethod
  def to_ascii(cls, permutation):
    return rothe_diagram(permutation)

class RS116(RS115):
  """
  Permutations a1 a2 ... am-1 of [m-1] with longest decreasing subsequence of
    length at most 2 (no integers i < j < k such that aj < ak < ai)
  
  Data Type:
    tuple(int)
  Format:
    sequences of integers in the set [1,m-1]. [0] is considered the empty
    set, and [1] = {1}
  Generator:
    ()
  Example: (m=5)
    (3,2,4,1)
  """

  ID = 'RS116'
  names = ['312 Avoiding Permutations']
  keywords = {'permutation', 'sequence', 'avoiding', '312', 'three', 'one', 'two'}

  generator = lambda: ()
  
  @classmethod
  def product(cls, fst, snd):
    return fst + tuple(x+len(fst)+1 for x in snd) + (len(fst)+1,)

  @classmethod
  def factorise(cls, permutation):
    split = permutation[-1]

    fst = tuple(x for x in permutation if x < split)
    snd = tuple(x-len(fst)-1 for x in permutation if x > split)

    return (fst, snd)

class TwoThreeOneAvoiding(RS115):
  """
  Permutations a1 a2 ... am-1 of [m-1] with longest decreasing subsequence of
    length at most 2 (no integers i < j < k such that ak < ai < aj)
  
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

  ID = 'MA??'
  names = ['231 Avoiding Permutations']
  keywords = {'permutation', 'sequence', 'avoiding', '231', 'two', 'three', 'one'}

  generator = lambda: ()
  product = lambda fst, snd: fst + (len(fst) + len(snd) + 1,) + tuple(x+len(fst) for x in snd)

  @classmethod
  def factorise(cls, perm):
    row_split = perm.index(len(perm))
    fst = perm[:row_split]
    snd = tuple(x-len(fst) for x in perm[row_split+1:])

    return (fst, snd)

class TwoOneThreeAvoiding(RS115):
  """
  Permutations a1 a2 ... am-1 of [m-1] with longest decreasing subsequence of
    length at most 2 (no integers i < j < k such that aj < ai < ak)
  
  Data Type:
    tuple(int)
  Format:
    sequences of integers in the set [1,m-1]. [0] is considered the empty
    set, and [1] = {1}
  Generator:
    ()
  Example: (m=5)
    (4,1,2,3)
  """

  ID = 'MA??'
  names = ['213 Avoiding Permutations']
  keywords = {'permutation', 'sequence', 'avoiding', '213', 'two', 'one', 'three'}

  generator = lambda: ()
  product = lambda fst, snd: (len(fst) + 1,) + tuple(x+len(fst)+1 for x in snd) + fst

  @classmethod
  def factorise(cls, perm):
    column_split = perm[0]
    row_split = len(perm)-column_split+1
    fst = perm[row_split:]
    snd = tuple(x-len(fst)-1 for x in perm[1:row_split])

    return (fst, snd)


class OneThreeTwoAvoiding(RS115):
  """
  Permutations a1 a2 ... am-1 of [m-1] with longest decreasing subsequence of
    length at most 2 (no integers i < j < k such that ai < ak < aj)
  
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

  ID = 'MA??'
  names = ['132 Avoiding Permutations']
  keywords = {'permutation', 'sequence', 'avoiding', '132', 'one', 'three', 'two'}

  generator = lambda: ()
  product = lambda fst, snd: tuple(x+len(fst) for x in snd) + (len(fst) + len(snd) + 1,) + fst

  @classmethod
  def factorise(cls, perm):
    row_split = perm.index(len(perm))
    fst = perm[row_split+1:]
    snd = tuple(x-len(fst) for x in perm[:row_split])

    return (fst, snd)