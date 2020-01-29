from magma import Catalan

class FriezePatterns(Catalan):
  generator = lambda: (0,0)
  
  @staticmethod
  def product(fst, snd):
    return (fst[0] + 1,) + fst[1:-1] + (fst[-1] + snd[0] + 1,) + snd[1:-1] + (snd[-1] + 1,)

  @classmethod
  def to_pattern_rows(cls, frieze_pattern):
    n = len(frieze_pattern)
    rows = (([[1] * n] if n > 2 else [])
            + [list(frieze_pattern)]
            + [None] * (n-5)
            + ([frieze_pattern[-2:] + frieze_pattern[:-2]] if n > 4 else [])
            + ([[1] * n] if n > 3 else [])
          )

    for i in range(2, n//2):
      #      (i-2,j+1)
      # (i-1,j)     (i-1,j+1)
      #        (i,j) <<-- calculating this
      rows[i] = [(rows[i-1][j]*rows[i-1][j+1]-1)//rows[i-2][j+1] for j in range(n-1)]

      #               (-(i+1),i) <<-- calculating this (it is the same number at the end of row[i])
      # (-i,i-1)          (-i,i)
      #            (-(i-1),i-1)
      rows[i].append((rows[-i][i-1] * rows[-i][i]-1)//rows[-(i-1)][i-1])
      rows[-(i+1)] = rows[i][-(i+1):] + rows[i][:-(i+1)]

    return rows

  
  
  @classmethod
  def to_ascii(cls, frieze_pattern, generator=False):
    if generator: return ''.join(map(str, frieze_pattern))

    def verify_rows(rows):
      for i in range(1,len(rows)-1):
        for s,t,r,u in zip(rows[i], rows[i][1:], rows[i-1][1:], rows[i+1]):
          if s*t-r*u != 1:
            return False
      return True

    rows = cls.to_pattern_rows(frieze_pattern)
    
    max_digits = len(str(len(frieze_pattern)-1))

    sep = ' ' * max_digits

    return '\n'.join(sep*i + sep.join(f'{x:<{max_digits}}' for x in row) for i, row in enumerate(rows))

  
    

22151313



