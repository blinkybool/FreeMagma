from magma import Catalan, AsciiDrawing

class StaircasePolygons(Catalan):
  generator = lambda: ('','')
  
  @classmethod
  def product(cls, fst, snd):
    if fst == cls.generator(): fst = ('N', '')
    if snd == cls.generator(): snd = ('E', 'E')
    
    fst_left, fst_right = fst
    snd_left, snd_right = snd


    return (fst_left + snd_left, fst_right[:-1] + snd_right + 'N')

  @classmethod
  def factorise(cls, polyomino):
    pass
    # left, right = polyomino
    # width = left.count('E')
    # height = left.count('N')

    # def backstep(pos, dir):
    #   return {'N': (pos[0]-1,pos[1]), 'E': (pos[0], pos[1]-1)}

    # left_walker, right_walker = (width, height)
    # left_iter = reversed(left)
    # right_ter = reversed(right)
    # for col in range(width, -1, -1):
    #   while (left_step := next(left_iter) == 'E'):



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