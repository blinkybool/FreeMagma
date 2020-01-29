from magma import Catalan, wrap_tikz_env

class CBTs(Catalan):
  @classmethod
  def tikz_command(cls, cbt, with_env=False):
    try:
      tikz_cbt = 'cbt ' + ''.join({'(': '[', ')': ']', ',': '', ' ':' '}[char] for char in str(cbt))
    except:
      raise ValueError

    return wrap_tikz_env('forest', tikz_cbt) if with_env else tikz_cbt

class PlaneTrees(Catalan):
  generator = lambda: ()
  product = lambda fst, snd: fst + (snd,)
  factorise  = lambda plane_tree: (plane_tree[:-1], plane_tree[-1])

  @classmethod
  def tikz_command(cls, plane_tree, with_env=False):
    try:
      tikz_pt = 'pt ' + ''.join({'(': '[', ')': ']', ',': '', ' ':' '}[char] for char in str(plane_tree))
    except:
      raise ValueError

    return wrap_tikz_env('forest', tikz_pt) if with_env else tikz_pt
