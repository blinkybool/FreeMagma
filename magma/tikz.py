def to_tikz_pair_loop(iterable):
  return ','.join(f'{fst}/{snd}' for (fst,snd) in iterable)

def wrap_tikz_env(env_name, content, options=None):
  options = f'[{options}]' if options is not None else ''
  return f'\\begin{{{env_name}}}{options}\n' + content.replace('\n', '\n  ') + f'\n\\end{{{env_name}}}'

def wrap_tikz_command(command_name, *args, optional=None):
  optional = f'[{optional}]' if optional is not None else ''
  return '\\' + str(command_name) + optional +  ''.join(f'{{{arg}}}' for arg in args)

def embed_lattice_path(steps, step_dir, start=(0,0), with_start=True):
  (x,y) = start

  if with_start:
    yield (x,y)
  
  for step in steps:
    dx, dy = step_dir[step]

    x += dx
    y += dy

    yield (x,y)
  
def tikz_path(coords, options=None):
  options = f'[{options}]' if options is not None else ''
  return f'\\draw{options} ' + ' -- '.join(f'({x},{y})' for x,y in coords) + ';'
