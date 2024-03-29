from magma import Catalan, AsciiDrawing, wrap_tikz_command, wrap_tikz_env, embed_lattice_path, to_tikz_pair_loop, tikz_path

class RS57(Catalan):
  """
  Unordered pairs of lattice paths with m steps each ((0,1) or (1,0)), both
    starting at (0,0) and ending at the same point, and otherwise never intersect. 
  
  Data Type:
    tuple(string)
  Format:
    an ordered pair of paths (the upper/left path is first in the pair)
    where a path is a word in the alphabet {N,E}, where N=(1,0), E=(0,1).
  Generator:
    ('E','E')
  Example: (m=5)
    ('NNNEE', 'ENENN')
     _ _ 
    |   |
    |  _|
    |_|  
  """
  
  ID = 'RS57'
  names = ['Staircase Polygons', 'Parallelogram Polyominoes']
  keywords = {'staircase', 'polgon', 'parallelogram', 'polyomino', 'lattice', 'path', 'ascii'}

  generator = lambda: ('E','E')
  
  @classmethod
  def product(cls, fst, snd):
    if fst == cls.generator(): fst = ('N', 'N')
    
    fst_left, fst_right = fst
    snd_left, snd_right = snd

    return (fst_left + snd_left, fst_right[:-1] + snd_right + 'N')

  @classmethod
  def factorise(cls, polyomino):
    left, right = polyomino
    width = left.count('E')
    height = left.count('N')

    left_walker = right_walker = (width, height)
      
    def move_back(walker, step_dir):
      if step_dir == 'N':
        return (walker[0], walker[1]-1)
      else:
        assert step_dir == 'E'
        return (walker[0]-1, walker[1])

    assert right[-1] == 'N'
    split = len(left)

    # Ignore the last (north) step in the right path, effectively undoing the
    # north shift done by the product, then backtrack the path with the walkers
    # until the bottom left corner of the snd factor is found.
    for left_step, right_step in zip(left[::-1], right[-2::-1]):

      left_walker = move_back(left_walker, left_step)
      right_walker = move_back(right_walker, right_step)

      split -= 1

      # found the bottom left corner of the snd factor
      if left_walker == right_walker:
        break

    fst = (left[:split], right[:split-1] + 'N')
    snd = (left[split:], right[split-1:-1])

    return (cls.generator() if fst==('N','N') else fst, snd)

  @classmethod
  def direct_norm(cls, polyomino):
    return len(polyomino[0])

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

  @classmethod
  def tikz(cls, polyomino, colour_factors=False, with_env=False):
    norm = cls.direct_norm(polyomino)
    lines = [f'\\draw[step=1,gray,thin] (0,0) grid ({norm-1},{norm-1});']
    left, right = polyomino
    leftCoords = list(embed_lattice_path(left, step_dir={'N': (0,1), 'E':(1,0)}))
    rightCoords = list(embed_lattice_path(right, step_dir={'N': (0,1), 'E':(1,0)}))

    
    if colour_factors and norm > 1:

      fst, _ = cls.factorise(polyomino)
      fst_norm = cls.direct_norm(fst)

      shiftedSndRightCoords = [(x,y+1) for x,y in rightCoords[fst_norm-1:-1]]

      lines.append(tikz_path(leftCoords[:fst_norm+1] + rightCoords[fst_norm-1::-1], options='draw=none, fill=\\fstColour, opacity=.2'))
      lines.append(tikz_path(leftCoords[fst_norm:] + shiftedSndRightCoords[::-1], options='draw=none, fill=\\sndColour, opacity=.2'))

      lines.append(tikz_path(leftCoords[:fst_norm+1], options='\\fstColour'))
      lines.append(tikz_path(rightCoords[:fst_norm], options='\\fstColour'))

      lines.append(tikz_path(leftCoords[fst_norm:], options='\\sndColour'))
      lines.append(tikz_path(rightCoords[fst_norm-1:-1], options='\\sndColour'))
      lines.append(tikz_path(rightCoords[-2:]))



      lines.append(f'\\draw[draw=none, fill=\\fstColour] {leftCoords[0]} circle;')
      lines.append(f'\\draw[draw=none, fill=\\bothColour] {leftCoords[fst_norm]} circle;')
      lines.append(f'\\draw[draw=none, fill=\\sndColour] {leftCoords[-1]} circle;')

    else:
      lines.append(tikz_path(leftCoords))
      lines.append(tikz_path(rightCoords))

      lines.append(f'\\draw[fill] {leftCoords[0]} circle;')
      lines.append(f'\\draw[fill] {leftCoords[-1]} circle;')


    if with_env:
      return wrap_tikz_env('tikzpicture', '\n'.join(lines))
    else:
      return '\n'.join(lines)
    



