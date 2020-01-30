from magma import Catalan, AsciiDrawing, wrap_tikz_command, wrap_tikz_env, to_tikz_pair_loop

class RS24(Catalan):
  '''
  Lattice Paths from (0,0) to (n-1,n-1) with steps (0,1), (1,0) that never rise
  above the diagonal
  Data Type: String
  Format: words in the alphabet {E,N} where E is a (0,1) step and N is a (1,0) step.
  '''
  RS = 24
  names = {'dyck paths', 'lattice paths'}
  keywords = {'dyck', 'paths', 'lattice', 'steps', 'geometric', 'E', 'N', 'ascii'}
  generator = lambda: ''
  product = lambda fst, snd: fst + 'E' + snd + 'N'

  @staticmethod
  def factorise(dyck_path):
    assert len(dyck_path) >= 2
    assert dyck_path[-1] == 'N'

    # step-distance to diagonal
    dist = 1 
    for i in range(len(dyck_path) - 2, -1, -1):
      dist += {'N': 1, 'E': -1}[dyck_path[i]]
      if dist <= 0: break
    else:
      raise ValueError
    
    return (dyck_path[0:i], dyck_path[i+1:-1])

  @staticmethod
  def to_ascii(dyck_path):
    drawing = AsciiDrawing(2*dyck_path.count('E')+1, dyck_path.count('N')+1)

    step_char = {'N': '|', 'E': '_'}
    step_dir = {'N': (0,1), 'E': (1,0)}

    x,y = (0,0)
    for step in dyck_path:
      if step == 'E':
        x += 1
      drawing.write(step_char[step], x, y)
      dx,dy = step_dir[step]
      x += dx
      y += dy

    x,y = (0,0)
    for _ in range(drawing.width):
      drawing.write('.', x, y)
      x += 2
      y += 1
    
    return str(drawing)

  @classmethod
  def tikz_command(cls, dyck_path, with_env=False):
    x,y = (0,0)

    step_dir = {'E': (1,0), 'N': (0,1)}

    path = []

    for step in dyck_path:
      dx,dy = step_dir[step]
      x += dx
      y += dy
      path.append((x,y))

    command = wrap_tikz_command('dyckPath', to_tikz_pair_loop(path))

    return wrap_tikz_env('tikzpicture', command) if with_env else command



class RS25(RS24):
  '''
  Lattice Paths from (0,0) to (2(n-1),0) with steps (1,1), (1,-1) that never fall
  below the x-axis.
  Data Type: String
  Format: words in the alphabet {U,D} where U is a (1,1) step and D is a (1,-1) step.
  '''
  RS = 24
  names = {'dyck paths', 'mountains'}
  keywords = {'mountains', 'dyck', 'paths', 'lattice', 'steps', 'geometric', 'U', 'D'}
  generator = lambda: ''
  product = lambda fst, snd: fst + 'U' + snd + 'D'

  @classmethod
  def factorise(mountain):
    assert len(mountain) >= 2
    assert mountain[-1] == 'D'

    height = 1 
    for i in range(len(mountain) - 2, -1, -1):
      height += {'U': 1, 'D': -1}[mountain[i]]
      if height <= 0: break
    else:
      raise ValueError
    
    return (mountain[0:i], mountain[i+1:-1])
    

  @staticmethod
  def to_ascii(mountain, trim_rows=True):
    drawing = AsciiDrawing(len(mountain), len(mountain)//2)
    x = 0
    y = 0

    step_char = {'U': '/', 'D': '\\'}
    step_y_dir = {'U': 1, 'D': -1}

    drawing.write('/', 0, 0)
    for prev_step, step in zip(mountain, mountain[1:]):
      x += 1
      if prev_step == step:
        y += step_y_dir[step]
      drawing.write(step_char[step], x, y)

    return drawing.get_str(trim_rows=trim_rows)