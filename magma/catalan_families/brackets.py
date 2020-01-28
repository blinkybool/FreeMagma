from magma import Catalan

class Brackets(Catalan):
  generator = lambda: ''
  product = lambda fst, snd: fst + '{' + snd + '}'

  @classmethod
  def factorise(cls, brackets):
    assert len(brackets) >= 2
    assert brackets[-1] == '}'
  
    unpaired = 1
    for i in range(len(brackets) - 2, -1, -1):
      unpaired += {'{': -1, '}': 1}[brackets[i]]
      if unpaired <= 0: break
    else:
      raise ValueError
    
    return (brackets[0:i], brackets[i+1:-1])