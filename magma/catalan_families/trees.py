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

class RS4(RS5):
  """
  Binary Trees with m-1 vertices.

  Data Type:
    None | tuple() | tuple(..., ...) (recursive)
  Format:
    a BT is either None, an empty tuple (leaf node) or a pair of BTs indicating
    the left and right subtree.
  Generator:
    None
  Examples:
    (m=1)
    None
    <empty>

    (m=2)
    ()
    *

    (m=3)
    ((), None)
      *
     /
    *
  """

  ID = 'RS4'
  names = ['Binary Trees']
  keywords = {'binary', 'tree'}

  generator = lambda: None
  product = lambda fst, snd: () if fst==snd==None else (fst, snd)
  factorise = lambda tree: (None, None) if tree==() else tree

  @classmethod
  def tikz_command(cls, cbt, with_env=False):
    raise NotImplementedError

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

class RS7(RS6):
  r"""
  Planted (root has one child) trivalent (internal vertices have 3 adjacent
    vertices - ie. two children) Plane Trees with 2m vertices. Basically CBTs
    (see RS5) with a new root.
  
  Data Type:
    tuple(tuple(...)) (recursive)
  Format:
    a singleton tuple with a CBT in it. A CBT is a tuple of 0 or 2 CBTs.
  Generator:
    ((),)
  Examples:
    (m=1)
    ((),)
    *
    |
    *

    (m=2)
    (((),()),)
      *
      |
      *
     / \
    *   *
  """

  ID = 'RS7'
  names = ['Planted Trivalent Plane Trees']
  keywords = {'planted', 'trivalent', 'plane', 'tree'}

  generator = lambda: ((),)
  product = lambda fst, snd: (fst[0], snd[0])
  factorise = lambda tree: tree[0]

class RS12(RS6):
  r"""
  Plane Trees with m-1 internal vertices, such that
    (1) each vertex has at most 2 children
    (2) each left child of a vertex with 2 children is an internal vertex.
  
  Data Type:
    tuple(tuple(...)) (recursive)
  Format:
    a tuple of zero or more tuples.
  Generator:
    ()
  Example: (m=4)
    ( ( ( ((),) , () ) , () ) , () )
        *
       / \
      *   *
     / \
    *   *
    |
    *
  """
  
  ID = 'RS12'
  names = ['Left-Internal Unary-Binary Tree']
  keywords = {'left', 'internal', 'unary', 'binary', 'tree'}

  generator = lambda: ()
  product = lambda fst, snd: (snd,) if fst == () else (fst, snd)
  factorise = lambda tree: ((), tree[0]) if len(tree)==1 else tree

