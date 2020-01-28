from magma import Catalan, to_tikz_pair_loop, wrap_tikz_env, wrap_tikz_command

class NestedMatchings(Catalan):
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

class Arches(NestedMatchings):
  @classmethod
  def tikz_command(cls, arches, with_env=False):
    command = wrap_tikz_command('arches', 2*len(arches), to_tikz_pair_loop(arches))
    return wrap_tikz_env('tikzpicture', command) if with_env else command
  
class NonCrossingChords(NestedMatchings):
  @classmethod
  def tikz_command(cls, chords, radius=2, with_env=False):
    command = wrap_tikz_command('nonCrossingChords', radius, 2*len(chords), to_tikz_pair_loop(chords))
    return wrap_tikz_env('tikzpicture', command) if with_env else command