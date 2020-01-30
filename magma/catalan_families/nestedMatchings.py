from magma import Catalan, to_tikz_pair_loop, wrap_tikz_env, wrap_tikz_command

class RS61(Catalan):
  r"""
  Noncrossing, complete, matchings on 2(n-1) vertices, i.e. ways of connecting
    2(n-1) vertices on a line by n-1 non-intersecting arcs all lying above the line
  Data Type: tuple(tuple(int))
  Format: sequences of n-1 pairs of integers from 1 to 2(n-1) where a pair (i,j)
    represents an arc from vertex i to vertex j. No order is imposed on the sequence
    of pairs, nor on the pairs themselves.
  Generator: ()
  Example:
    ((6,3), (4,5), (1,2))
                 __________
      __        /    __    \ 
     /  \      /    /  \    \ 
    1----2----3----4----5----6
  """
  RS = 61
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
  def tikz_command(cls, arches, with_env=False):
    command = wrap_tikz_command('arches', 2*len(arches), to_tikz_pair_loop(arches))
    return wrap_tikz_env('tikzpicture', command) if with_env else command
  
class RS59(RS61):
  r"""
  Noncrossing, complete, matchings on 2(n-1) vertices on a circle, i.e. ways of
    connecting 2(n-1) vertices on a circle by non-intersecting chords.
  Data Type: tuple(tuple(int))
  Format: sequences of n-1 pairs of integers from 1 to 2(n-1) where a pair (i,j)
    represents a chord from vertex i to vertex j. No order is imposed on the
    sequence of pairs, nor on the pairs themselves.
  Generator: ()
  Example:
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
  RS = 61
  names = ['Noncrossing Chords']
  keywords = {'nested', 'noncrossing', 'nonintersecting' 'matching', 'chords'}

  @classmethod
  def tikz_command(cls, chords, radius=2, with_env=False):
    command = wrap_tikz_command('nonCrossingChords', radius, 2*len(chords), to_tikz_pair_loop(chords))
    return wrap_tikz_env('tikzpicture', command) if with_env else command