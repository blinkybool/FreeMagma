from magma import Catalan, AsciiDrawing, wrap_tikz_command, wrap_tikz_env, to_tikz_pair_loop

class DyckPaths(Catalan):
  generator = lambda: ''
  product = lambda fst, snd: fst + 'N' + snd + 'E'

  @staticmethod
  def factorise(dyck_path):
    assert len(dyck_path) >= 2
    assert dyck_path[-1] == 'E'

    height = 1
    for i in range(len(dyck_path) - 2, -1, -1):
      height += {'N': 1, 'E': -1}[dyck_path[i]]
      if height <= 0: break
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

    x,y = (1,0)
    for _ in range(drawing.width):
      drawing.write('.', x, y)
      x += 2
      y += 1
    
    return str(drawing)

  @classmethod
  def tikz_command(cls, dyck_path, with_env=False):
    x,y = (0,0)

    step_dir = {'N': (0,1), 'E': (1,0)}

    path = []

    for step in dyck_path:
      dx,dy = step_dir[step]
      x += dx
      y += dy
      path.append((x,y))

    command = wrap_tikz_command('dyckPath', to_tikz_pair_loop(path))

    return wrap_tikz_env('tikzpicture', command) if with_env else command



class Mountains(DyckPaths):
  @staticmethod
  def to_ascii(dyck_path, trim_rows=True):
    drawing = AsciiDrawing(len(dyck_path), len(dyck_path)//2)
    x = 0
    y = 0

    step_char = {'N': '/', 'E': '\\'}
    step_y_dir = {'N': 1, 'E': -1}

    drawing.write('/', 0, 0)
    for prev_step, step in zip(dyck_path, dyck_path[1:]):
      x += 1
      if prev_step == step:
        y += step_y_dir[step]
      drawing.write(step_char[step], x, y)

    return drawing.get_str(trim_rows=trim_rows)