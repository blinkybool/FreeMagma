from magma import Catalan

class MatchingBrackets(Catalan):
  r"""
  Arrangements of m-1 pairs of left and right brackets which are 'valid'/'matched'
    i.e. a bracket word w is valid iff it has an equal number of left and right
    brackets, and all factorisation w=uv has - in the left factor, u - at least
    as many left brackets, '(', as it does right brackets ')'. More formally,
      (1) count('(', w) == count(')', w)
      (2) \forall w=uv : count('(', u) >= count(')', u)
    
  Data Type:
    String
  Format:
    words in the alphabet {(,)}
  Example: (m=5)
    ()()(())
  """
  ID = 'MA5'
  names = ['Matching Brackets', 'Balanced Parentheses']
  keywords = {'ascii', 'brackets', '(', ')', '()'}
  generator = lambda: ''
  product = lambda fst, snd: fst + '(' + snd + ')'

  @classmethod
  def factorise(cls, brackets):
    assert len(brackets) >= 2
    assert brackets[-1] == ')'
  
    unpaired = 1
    for i in range(len(brackets) - 2, -1, -1):
      unpaired += {'(': -1, ')': 1}[brackets[i]]
      if unpaired <= 0: break
    else:
      raise ValueError
    
    return (brackets[0:i], brackets[i+1:-1])