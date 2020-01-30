from magma import Catalan

class MatchingBrackets(Catalan):
  """
  Arrangements of m-1 pairs of left and right brackets which are 'valid'/'matched'
    i.e. scanning from left to right, there are always more left brackets than
    right brackets in the cummulative counts
    
  Data Type:
    String
  Format:
    words in the alphabet {(,)}
  Example: (m=5)
    ()()(())
  """
  ID = 'MA5'
  names = ['Matching Brackets', 'Balanced Parenthesis']
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