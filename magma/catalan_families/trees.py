from magma import Catalan, wrap_tikz_env

class RS5(Catalan):
  r"""
  Complete Binary Trees with 2m-1 nodes.

  Data Type:
    tuple(tuple(...)) (recursive)
  Format:
    either empty tuple (a single node), or a pair of CBTs
  Generator:
    ()
  Example: (n=3)
    ((),((),()))
      * 
     / \
    *   *
       / \
      *   *
  """
  ID = 'RS5'
  names = ['Complete Binary Trees', 'CBTs']
  keywords = {'complete', 'binary', 'tree', 'recursive', 'tikz'}

  @classmethod
  def tikz_command(cls, cbt, with_env=False):
    try:
      tikz_cbt = 'cbt ' + ''.join({'(': '[', ')': ']', ',': '', ' ':' '}[char] for char in str(cbt))
    except:
      raise ValueError

    return wrap_tikz_env('forest', tikz_cbt) if with_env else tikz_cbt

class RS6(Catalan):
  r"""
  Plane Trees with m-nodes.

  Data Type:
    tuple(tuple(...)) (recursive)
  Format:
    a tuple of 0 or more tuples - representing the tree structurally
  Generator:
    ()
  Example: (n=7)
    ((),((),((),)), ())
        * 
      / | \
     *  *  *
       / \
      *   *
          |
          *
    Note that a python tuple with one element, x, is written (x,), and not (x)
  """
  ID = 'RS6'
  names = ['Plane Trees']
  keywords = {'plane', 'tree', 'tikz'}

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
