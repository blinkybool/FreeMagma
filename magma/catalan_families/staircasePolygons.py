from magma import Catalan, AsciiDrawing

class RS57(Catalan):
  """
  Unordered pairs of lattice paths with n steps each ((0,1) or (1,0)), both
    starting at (0,0) and ending at the same point, and otherwise never intersect. 
  Data Type: tuple(string)
  Format: an ordered pair of paths (the upper/left path is first in the pair)
    where a path is a word in the alphabet {N,E}, where N=(1,0), E=(0,1).
  Generator: ('E','E')
  Example: (n=5) ('NNNEE', 'ENENN)
     _ _ 
    |   |
    |  _|
    |_|  
  """
  RS = 57
  names = ['Staircase Polygons', 'Parallelogram Polyominoes']
  keywords = {'staircase', 'polgon', 'parallelogram', 'polyomino', 'lattice', 'path', 'ascii'}

  generator = lambda: ('E','E')
  
  @classmethod
  def product(cls, fst, snd):
    if fst == cls.generator(): fst = ('N', '')
    
    fst_left, fst_right = fst
    snd_left, snd_right = snd


    return (fst_left + snd_left, fst_right[:-1] + snd_right + 'N')

  @classmethod
  def factorise(cls, polyomino):
    left, right = polyomino
    width = left.count('E')
    height = left.count('N')

    left_walker = right_walker = (width, height)

    left_fst = list(left)
    left_snd = []
    right_fst = list(right)
    right_snd = []

    def gap_size():
      return left_walker[1] - right_walker[1]

    def backstep(walker, path_fst, path_snd):
      step_dir = path_fst.pop()
      path_snd.append(step_dir)
      if step_dir == 'N':
        return (walker[0], walker[1]-1)
      else:
        assert step_dir == 'E'
        return (walker[0]-1, walker[1])

    while len(left_fst) > 0:

      # move east
      left_walker = backstep(left_walker, left_fst, left_snd)

      while left_fst and left_fst[-1] == 'N':
        left_walker = backstep(left_walker, left_fst, left_snd)

      while right_walker[0] != left_walker[0]:
        right_walker = backstep(right_walker, right_fst, right_snd)

      if gap_size() <= 1: break

    if left_fst == right_fst == []:
      fst = ('E', 'E')
      snd = (''.join(reversed(left_snd[:-1])), ''.join(reversed(right_snd[1:])))
    else:
      fst = (''.join(left_fst), ''.join(right_fst) + 'N')
      snd = (''.join(reversed(left_snd)), ''.join(reversed(right_snd[1:])))

    return fst, snd


  @classmethod
  def to_ascii(cls, polyomino):
    if polyomino == cls.generator(): return '_'
    left, right = polyomino

    ascii_drawing = AsciiDrawing(2*left.count('E')+1, left.count('N')+1)

    step_char = {'N': '|', 'E': '_'}
    step_dir = {'N': (0,1), 'E': (1,0)}

    for path in (left, right):
      x,y = (0,0)
      for step in path:
        if step == 'E':
          x += 1
        ascii_drawing.write(step_char[step], x, y)
        dx,dy = step_dir[step]
        x += dx
        y += dy
    
    return str(ascii_drawing)