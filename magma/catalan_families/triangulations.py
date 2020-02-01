from magma import Catalan, TEX_TEMPLATES_PATH, wrap_tikz_command, wrap_tikz_env, to_tikz_pair_loop

class RS1(Catalan):
  """
  Permutations a1 a2 ... am-1 of [m-1] with longest decreasing subsequence of
    length at most 2 (no integers i < j < k such that ai > aj > ak).
  
  Data Type:
    tuple(int)
  Format:
    sequences of integers in the set [1,m-1]
  Generator:
    ()
  Example: (m=5)
    (3,1,2,4)
  """
  ID = 'RS1'
  names = ['Triangulations']
  keywords = {'triangulation', 'triangle', 'polygon', 'tikz'}
  generator = lambda: ()
  
  @classmethod
  def product(cls, fst, snd):
    num_fst = len(fst) + 2
    num_snd = len(snd) + 2
    num_out = num_fst + num_snd - 1
    return fst + tuple((src+num_fst-1, tar+num_fst-1) for src,tar in snd) + ((1, num_out),)

  @classmethod
  def factorise(cls, triangulation):
    num_vertices = len(triangulation) + 2
    split = max((max(chord) for chord in triangulation if 1 in chord and num_vertices not in chord), default=2)

    fst = tuple(chord for chord in triangulation if max(chord) <= split)
    snd = tuple((src-split+1, tar-split+1) for src,tar in triangulation if split <= min(src,tar))

    return (fst, snd)

  @staticmethod
  def tikz_command(triangulation, radius='2', with_env=False):
    num_vertices = len(triangulation) + 2
    chords_tex_format = to_tikz_pair_loop(chord for chord in triangulation if (min(chord), max(chord)) != (1,num_vertices))
    command = wrap_tikz_command('triangulation', radius, num_vertices, chords_tex_format)
    if with_env:
      return wrap_tikz_env('tikzpicture', command)
    else:
      return command
    

  @staticmethod
  def tikz_full(triangulation, radius='2', vertex_radius='3pt', label_offset='.5'):
    with open(TEX_TEMPLATES_PATH + '/triangulation-full.tex') as template:
      num_vertices = len(triangulation) + 2
      chords_tex_format = to_tikz_pair_loop(chord for chord in triangulation if (min(chord), max(chord)) != (1,num_vertices))
      output = (template.read()
                .replace('SUB_RADIUS',        str(radius))
                .replace('SUB_VERTEX_RADIUS', str(vertex_radius))
                .replace('SUB_LABEL_OFFSET',  str(label_offset))
                .replace('SUB_NUM_VERTICES',  str(num_vertices))
                .replace('SUB_CHORDS', chords_tex_format)
               )
    return output