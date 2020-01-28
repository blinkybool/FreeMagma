from magma import Catalan

class FriezePatterns(Catalan):
  generator = lambda: (0,0)
  
  @staticmethod
  def product(fst, snd):
    return (fst[0] + 1,) + fst[1:-1] + (fst[-1] + snd[0] + 1,) + snd[1:-1] + (snd[-1] + 1,)
  
  @classmethod
  def to_ascii(cls, frieze_pattern):
    return ''.join(map(str, frieze_pattern))