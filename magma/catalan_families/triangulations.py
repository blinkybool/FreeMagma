from magma import Catalan, TEX_TEMPLATES_PATH, wrap_tikz_command, wrap_tikz_env, to_tikz_pair_loop

class RS1(Catalan):
  r"""
  Triangulations of an (m+1)-gon (with m-1 triangles).
  
  Data Type:
    tuple(tuple(int))
  Format:
    tuple of pairs of vertex numbers, where a pair (i,j) is either an internal
    chord from vertex i to vertex j, or the outer edge from the initial vertex 1
    to the last numbered vertex (m+1).

    The vertices are numbered 1 to (m+1), counterclockwise, such
    that (1,m+1) edge is positioned horizontally at the top (see example).

    If m > 1, the top edge is included amongst the list of internal chords.

    The order of the chords does not matter, neither does the order of source
    and target vertices within a chord. This means equality of triangulation
    objects is not python object equality.

  Generator:
    ()
  Examples:
    (m=1)
    ()
    1 -- 2

    (m=2)
    ((1,3),)
    1 --- 3
     \   /
       2

    (m=3)
    ((1,4),(2,4))
    1 ------ 4
    |      . |
    |    .   |
    |  .     |
    |.       |
    2 ------ 3
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

  @classmethod
  def normalise(cls, triangulation):
    return tuple(sorted((min(chord), max(chord)) for chord in triangulation))

  @classmethod
  def direct_norm(cls, triangulation):
    return triangulation.count('o')

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