def to_tikz_pair_loop(iterable):
  return ','.join(f'{fst}/{snd}' for (fst,snd) in iterable)

def wrap_tikz_env(env_name, content):
  return f'\\begin{{{env_name}}}\n{content}\n\\end{{{env_name}}}'

def wrap_tikz_command(command_name, *args, optional=None):
  optional = f'[{optional}]' if optional is not None else ''
  return '\\' + str(command_name) + optional +  ''.join(f'{{{arg}}}' for arg in args)