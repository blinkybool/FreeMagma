from magma import Catalan, to_tikz_pair_loop, wrap_tikz_env, wrap_tikz_command

class RS61(Catalan):
  r"""
  Noncrossing, complete, matchings on 2(m-1) vertices, i.e. ways of connecting
    2(m-1) vertices on a line by m-1 non-intersecting arcs all lying above the
    line.

  Data Type:
    tuple(tuple(int))
  Format:
    sequences of m-1 pairs of integers from 1 to 2(m-1) where a pair (i,j)
    represents an arc from vertex i to vertex j. No order is imposed on the sequence
    of pairs, nor on the pairs themselves.
  Generator:
    ()
  Example: (m=4)
    ((6,3), (4,5), (1,2))
                 __________
      __        /    __    \ 
     /  \      /    /  \    \ 
    1----2----3----4----5----6
  """
  ID = 'RS61'
  names = ['Nested Matchings', 'Nested Arches', 'Nested Arcs']
  keywords = {'nested', 'matching', 'arch', 'arc'}
  generator = lambda: ()
  
  @classmethod
  def product(cls, fst, snd):
    size_fst = len(fst) * 2
    size_snd = len(snd) * 2
    return fst + ((size_fst+1, size_fst+size_snd+2),) + tuple((src+size_fst+1, tar+size_fst+1) for src,tar in snd)

  @classmethod
  def factorise(cls, matching):
    split_match = max(matching, key=lambda match: max(match))
    left_split, right_split = (min(split_match), max(split_match))
    fst = tuple(match for match in matching if max(match) < left_split)
    snd = tuple((src-left_split, tar-left_split) for src,tar in matching if left_split < min(src,tar) and max(src,tar) < right_split)
    return fst, snd

  @classmethod
  def normalise(cls, matching):
    return tuple(sorted((min(match), max(match)) for match in matching))

  @classmethod
  def direct_norm(cls, matching):
    return len(matching)//2 + 1

  @classmethod
  def tikz_command(cls, arches, with_env=False):
    command = wrap_tikz_command('arches', 2*len(arches), to_tikz_pair_loop(arches))
    return wrap_tikz_env('tikzpicture', command) if with_env else command
  
class RS59(RS61):
  r"""
  Noncrossing, complete, matchings on 2(m-1) vertices on a circle, i.e. ways of
    connecting 2(m-1) vertices on a circle by non-intersecting chords.
  Data Type:
    tuple(tuple(int))
  Format: sequences of m-1 pairs of integers from 1 to 2(m-1) where a pair (i,j)
    represents a chord from vertex i to vertex j. No order is imposed on the
    sequence of pairs, nor on the pairs themselves.
  Generator:
    ()
  Example: (m=4)
    ((6,3), (4,5), (1,2))
         .....    
      . 1     6 .   
     ' /     /   '
    ' /     /     '
    2      /      5
    '     /     / '
     '   /     / '
      ' 3     4 ' 
         '''''
  """
  ID = 'RS59'
  names = ['Noncrossing Chords']
  keywords = {'nested', 'noncrossing', 'nonintersecting' 'matching', 'chords'}

  @classmethod
  def tikz_command(cls, chords, radius=2, with_env=False):
    command = wrap_tikz_command('nonCrossingChords', radius, 2*len(chords), to_tikz_pair_loop(chords))
    return wrap_tikz_env('tikzpicture', command) if with_env else command


class RS62(Catalan):
  r"""
  Graphs on m vertices lying on an (invisible) horizontal line L with m-1 arcs
    connecting the vertices such that:
    (a) the arcs do not pass below L (they can sit along L)
    (b) the graph is a tree
    (c) no two arcs intersect in their interiors
    (d) at a vertex, all vertices exit in the same direction
  
  Data Type:
    tuple(tuple(int))
  Format:
    an unordered list of unordered pairs of vertices, where each pair (i,j)
    represents an arc from the ith vertex to the jth vertex
  Generator: ()
  Example: (m=4)
    ((1,3), (5,1), (2,3))
        ________
       /        \
      /______    \
     //      \    \
    1    2----3    4
  """
  ID = 'RS62'
  names = ['Outflow Non-Crossing Trees']
  keywords = {'arc', 'arch', 'graph', 'noncrossing', 'crossing', 'vertices'}
  generator = lambda: ()

  @classmethod
  def product(cls, fst, snd):
    max_fst = len(fst)+1
    max_snd = len(snd)+1
    return fst + ((1,max_fst + max_snd),) + tuple((src+max_fst, tar+max_fst) for src, tar in snd)

  @classmethod
  def factorise(cls, matching):
    max_vert = len(matching)+1

    split = max((max(arc) for arc in matching if 1 in arc and max_vert not in arc), default=1)

    fst = tuple(arc for arc in matching if max(arc) <= split)
    snd = tuple((src-split, tar-split) for src,tar in matching if split < min(src,tar))

    return (fst, snd)

  @classmethod
  def normalise(cls, matching):
    return tuple(sorted((min(match), max(match)) for match in matching))

  @classmethod
  def direct_norm(cls, matching):
    return len(matching) + 1