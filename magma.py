#!/usr/bin/env python3
from itertools import chain

class Catalan:
  generator = lambda: ()
  product = lambda fst, snd: (fst, snd)
  factorise = lambda arg: arg

  @classmethod
  def bijection(cls, Target_Catalan):
    def _bijection(domain_elt):
      if domain_elt == cls.generator():
        return Target_Catalan.generator()
      else:
        fst, snd = cls.factorise(domain_elt)
        return Target_Catalan.product(_bijection(fst), _bijection(snd))
    return _bijection

  @classmethod
  def identity(cls):
    return cls.bijection(cls)

  @classmethod
  def products(cls, n):
    if n in cls.generator_cache: return cls.generator_cache[n]

    cls.generator_cache[n] = list(cls.product(fst, snd)
      for i in range(n)
        for fst in cls.products(i)
          for snd in cls.products(n - i - 1)
    )
    return cls.generator_cache[n]

class ObjectFormatError(Exception):
  def __init__(self, cls, obj):
    self.cls = cls
    self.obj = obj

class FactoriseError(Exception):
  pass

class PrefixString(Catalan):
  generator = lambda: 'ε'
  product = lambda fst, snd: '*' + fst + snd

class InfixString(Catalan):
  generator = lambda: 'ε'
  product = lambda fst, snd: '(' + fst + '*' + snd + ')'

class PostfixString(Catalan):
  generator = lambda: 'ε'
  product = lambda fst, snd: fst + snd + '*'

class Brackets(Catalan):
  generator = lambda: ''
  product = lambda fst, snd: fst + '{' + snd + '}'

  @classmethod
  def factorise(cls, brackets):
    if brackets == cls.generator():
      raise FactoriseError
    if brackets[-1] != '}':
      raise ObjectFormatError(cls, brackets)

    unpaired = 1
    for i in range(len(brackets) - 2, -1, -1):
      try:
        unpaired += {'{': -1, '}': 1}[brackets[i]]
      except:
        raise ObjectFormatError(cls, brackets)
      if unpaired <= 0: break
    else:
      raise ObjectFormatError(cls, brackets)
    
    return (brackets[0:i], brackets[i+1:-1])

class MountainsAscii(Catalan):
  generator = lambda: ''

  @classmethod
  def product(cls, fst, snd):
    fst_rows = fst.split('\n')

    if snd == cls.generator():
      snd_rows = [ '/\\' ]
    else:
      snd_rows = [' ' + row + ' ' for row in snd.split('\n')]
      snd_rows.append('/' + ' ' * (len(snd_rows[0]) - 2) + '\\')

    height = max(len(fst_rows), len(snd_rows))

    fst_rows = [' ' * len(fst_rows[0])] * (height - len(fst_rows)) + fst_rows
    snd_rows = [' ' * len(snd_rows[0])] * (height - len(snd_rows)) + snd_rows

    return '\n'.join(fst_row + snd_row for fst_row, snd_row in zip(fst_rows, snd_rows))

  @staticmethod
  def factorise(mountain):
    rows = mountain.split('\n')

    split = rows[-1].rfind('/')
    fst_rows = [row[0:split] for row in rows]
    snd_rows = [row[split+1:-1] for row in rows[:-1]]

    for piece_rows in fst_rows, snd_rows:
      # Remove whitespace rows
      while len(piece_rows) > 1 and (piece_rows[0].isspace() or piece_rows[0] == ''):
        piece_rows.pop(0)

    return ('\n'.join(fst_rows),'\n'.join(snd_rows))

class AsciiDrawing:
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.charmap = dict()

  def write(self, char, x, y):
    self.charmap[(x,y)] = char

  def __str__(self):
    return self.get_str()

  def get_str(self, trim_rows=False):
    rows = [''.join(self.charmap.get((x, self.height-y-1), ' ') for x in range(self.width)) for y in range(self.height)]
    if trim_rows:
      return '\n'.join(row for row in rows if not row.isspace())
    else:
      return '\n'.join(rows)

class DyckPath(Catalan):
  generator = lambda: ''
  product = lambda fst, snd: fst + 'N' + snd + 'E'

  @staticmethod
  def factorise(dyck_path):
    unpaired = 1
    for i in range(len(dyck_path) - 2, -1, -1):
      unpaired += 1 if dyck_path[i]=='E' else -1
      if unpaired <= 0: break
    
    return (dyck_path[0:i], dyck_path[i+1:-1])\

  @staticmethod
  def to_ascii(dyck_path):
    drawing = AsciiDrawing(2*dyck_path.count('E')+1, dyck_path.count('N')+1)

    step_char = {'N': '|', 'E': '_'}
    step_dir = {'N': (0,1), 'E': (1,0)}

    x,y = (0,0)
    for step in dyck_path:
      if step == 'E':
        x += 1
      drawing.write(step_char[step], x, y)
      dx,dy = step_dir[step]
      x += dx
      y += dy

    x,y = (1,0)
    for _ in range(drawing.width):
      drawing.write('.', x, y)
      x += 2
      y += 1
    
    return str(drawing)

class Mountain(DyckPath):

  @staticmethod
  def to_ascii(dyck_path, trim_rows=True):
    drawing = AsciiDrawing(len(dyck_path), len(dyck_path)//2)
    x = 0
    y = 0

    step_char = {'N': '/', 'E': '\\'}
    step_y_dir = {'N': 1, 'E': -1}

    drawing.write('/', 0, 0)
    for prev_step, step in zip(dyck_path, dyck_path[1:]):
      x += 1
      if prev_step == step:
        y += step_y_dir[step]
      drawing.write(step_char[step], x, y)

    return drawing.get_str(trim_rows=trim_rows)

class StaircasePolygon(Catalan):
  generator = lambda: ('','')
  
  @classmethod
  def product(cls, fst, snd):
    if fst == cls.generator(): fst = ('N', '')
    if snd == cls.generator(): snd = ('E', 'E')
    
    fst_left, fst_right = fst
    snd_left, snd_right = snd

    split = 0
    while split < len(snd_right) and snd_right[split] == 'E':
      split += 1

    return (fst_left + snd_left, fst_right[:-1] + snd_right[:split] + 'N' + snd_right[split:])

  @classmethod
  def to_ascii(cls, polyomino):
    if polyomino == cls.generator(): return '_'
    left, right = polyomino

    ascii_drawing = AsciiDrawing(2*left.count('E')+1, left.count('N')+1)

    step_char = {'N': '|', 'E': '_'}
    step_dir = {'N': (0,1), 'E': (1,0)}

    for path in (left, right):
      x,y = (0,0)
      for step in path:
        if step == 'E':
          x += 1
        ascii_drawing.write(step_char[step], x, y)
        dx,dy = step_dir[step]
        x += dx
        y += dy
    
    return str(ascii_drawing)

class CBT(Catalan):

  @staticmethod
  def tikz(cbt, with_env=False, with_full=False):
    tikz_cbt = ''.join({'(': '[', ')': ']', ',': '', ' ':' '}[char] for char in str(cbt))

    if with_full:
      with open('tex_templates/cbt-full.tex') as template:
        tikz_output = template.read().replace('SUBSTITUTE_CBT', tikz_cbt)
      return tikz_output
    elif with_env:
      with open('tex_templates/cbt-env.tex') as template:
        tikz_output = template.read().replace('SUBSTITUTE_CBT', tikz_cbt)
      return tikz_output
    else:
      return tikz_cbt

class Triangulation(Catalan):
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
  def tikz(triangulation, radius='2cm', vertex_radius='3pt', label_offset='.4cm'):
    with open('tex_templates/triangulation-env.tex') as template:
      num_vertices = len(triangulation) + 2
      chords_tex_format = ','.join(f'{src}/{tar}' for src, tar in triangulation if sorted((src,tar)) != (1,num_vertices))
      output = (template.read()
                .replace('SUB_RADIUS',        str(radius))
                .replace('SUB_VERTEX_RADIUS', str(vertex_radius))
                .replace('SUB_LABEL_OFFSET',  str(label_offset))
                .replace('SUB_NUM_VERTICES',  str(num_vertices))
                .replace('SUB_CHORDS', chords_tex_format)
               )
    return output


for Catalan_Family in [Catalan] + Catalan.__subclasses__():
  Catalan_Family.generator_cache = {0: [Catalan_Family.generator()]}

if __name__ == "__main__":
  # brackets_to_mountains = Brackets.get_fmap(Mountains)
  # for brackets in Brackets.products(8):
  #   print(brackets_to_mountains(brackets))
  # for n in range(5):
  #   print(Brackets2.products(n))

  # for tree in CBT.products(3):
  #   print(CBT.tikz(tree, with_env=True))

  # brackets_to_mountains = Brackets.get_fmap(Mountains)
  # print(brackets_to_mountains('{}{}{{{}{}}}'))

  # tri = ((1,3),)
  # fst, snd = Triangulation.factorise(tri)
  # print(tri)
  # print(fst)
  # print(snd)
  # print(Triangulation.product(fst,snd))

  # for n in range(4):
  #   print(Triangulation.products(n))

  # for trianglulation in Triangulation.products(3):
  #   print(Triangulation.tikz(trianglulation))
  # dyck_path = 'NENNEENENNNEEE'
  # for n in range(8):
  #   print('size:', n)
  #   polyominoes = StaircasePolygon.products(n)
  #   print('num of size:', len(polyominoes))
  #   print('=========================')
  #   for polyomino in polyominoes:
  #     # print(polyomino)
  #     print(StaircasePolygon.to_ascii(polyomino))
  #     print('------------')

  # drawing = AsciiDrawing(3,2)
  # drawing.write('|',0,0)
  # drawing.write('_',1,1)
  # drawing.write('_',1,0)
  # drawing.write('|',2,0)

  # print(str(drawing))

  print(len(DyckPath.products(6)))
  for dyck_path in DyckPath.products(6):
    print(DyckPath.to_ascii(dyck_path))
    print(dyck_path)