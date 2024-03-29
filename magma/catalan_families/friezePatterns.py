from magma import Catalan

# TODO inherit from Catalan once factorise written
class RS197:
  """
  Non-negative integer sequences (a_i) of length m+1 which generate a valid
    frieze pattern of m rows,

     1     1     1     1     1     1     1     1
       a_1   a_2   a_3    .     .     .     .    a_m+1
          b_1   b_2   b_3    .     .     .     .    b_m+1
              .     .     .     .     .     .     .     . 
                 .     .     .     .     .     .     .     . 
                   z_1   z_2   z_3    .     .     .     .    z_m+1
                       1     1     1     1     1     1     1     1
                       
    where any quadruple of the form below satisfies st-ru = 1.
         r
      s     t 
         u

  Data Type:
    tuple(int)
  Format:
    sequences of non-negative integers.
  Example: (m=5)
    (2,2,1,4,1,2)

    1 1 1 1 1 1
     2 2 1 4 1 2
      3 1 3 3 1 3
       1 2 2 2 1 4
        1 1 1 1 1 1
  """
  ID = 'RS197'
  names = ['Frieze Patterns']
  keywords = {'frieze', 'pattern', 'sequence', 'ascii'}
  generator = lambda: (0,0)

  @classmethod
  def factorise(cls, frieze_pattern):
    # TODO implement frieze pattern factorise
    pass
  
  @staticmethod
  def product(fst, snd):
    return (fst[0] + 1,) + fst[1:-1] + (fst[-1] + snd[0] + 1,) + snd[1:-1] + (snd[-1] + 1,)

  @classmethod
  def direct_norm(cls, frieze_pattern):
    return len(frieze_pattern) - 1

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

      #         (-(i+1),i) <<-- calculating this (it is the same number at the end of row[i])
      # (-i,i-1)          (-i,i)
      #        (-(i-1),i-1)
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

    assert verify_rows(rows)
    
    max_digits = len(str(len(frieze_pattern)-1))

    sep = ' ' * max_digits

    return '\n'.join(sep*i + sep.join(f'{x:{max_digits}}' for x in row) for i, row in enumerate(rows))