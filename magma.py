#!/usr/bin/env python3

class Catalan:
  generator = lambda: ()
  binary_op = lambda fst, snd: (fst, snd)
  factorise = lambda arg: arg

  @classmethod
  def get_fmap(cls, Target_Catalan):
    def fmap(domain_elt):
      if domain_elt == cls.generator():
        return Target_Catalan.generator()
      else:
        fst, snd = cls.factorise(domain_elt)
        return Target_Catalan.binary_op(fmap(fst), fmap(snd))
    return fmap

  @classmethod
  def identity(cls):
    return cls.get_fmap(cls)

  @classmethod
  def products(cls, n):
    if n in cls.generator_cache: return cls.generator_cache[n]

    cls.generator_cache[n] = list(cls.binary_op(fst, snd)
      for i in range(n)
        for fst in cls.products(i)
          for snd in cls.products(n - i - 1)
    )
    return cls.generator_cache[n]

class PrefixString(Catalan):
  generator = lambda: 'o'
  binary_op = lambda fst, snd: '*' + fst + snd

class InfixString(Catalan):
  generator = lambda: 'o'
  binary_op = lambda fst, snd: '(' + fst + '*' + snd + ')'

class PostfixString(Catalan):
  generator = lambda: 'o'
  binary_op = lambda fst, snd: fst + snd + '*'

class Brackets(Catalan):
  generator = lambda: ''
  binary_op = lambda fst, snd: fst + '{' + snd + '}'

  @staticmethod
  def factorise(brackets):
    unpaired = 1
    for i in range(len(brackets) - 2, -1, -1):
      unpaired += 1 if brackets[i]=='}' else -1
      if unpaired <= 0: break
    
    return (brackets[0:i], brackets[i+1:-1])

class Brackets2(Catalan, tuple):
  generator = lambda: Brackets2()
  binary_op = lambda fst, snd: Brackets2(fst + Brackets2((snd,)))
  factorise = lambda brackets: (brackets[:-1], brackets[-1])

  def __repr__(self):
    return ''.join('(' + repr(x) + ')' for x in self)

class Mountains(Catalan):
  generator = lambda: ''

  @classmethod
  def binary_op(cls, fst, snd):
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

class CBT(Catalan):

  @classmethod
  def tikz(cls, tree, with_env=False, with_full=False):
    tikz_tree = ''.join({'(': '[', ')': ']', ',': '', ' ':' '}[char] for char in str(tree))

    if with_full:
      with open('tex_templates/cbt-full.tex') as template:
        tikz_output = template.read().replace('SUBSTITUTE_CBT', tikz_tree)
      return tikz_output
    elif with_env:
      with open('tex_templates/cbt-env.tex') as template:
        tikz_output = template.read().replace('SUBSTITUTE_CBT', tikz_tree)
      return tikz_output
    else:
      return tikz_tree

    

for Catalan_Family in [Catalan] + Catalan.__subclasses__():
  Catalan_Family.generator_cache = {0: [Catalan_Family.generator()]}

if __name__ == "__main__":
  # brackets_to_mountains = Brackets.get_fmap(Mountains)
  # for brackets in Brackets.products(8):
  #   print(brackets_to_mountains(brackets))
  # for n in range(5):
  #   print(Brackets2.products(n))

  for tree in CBT.products(3):
    print(CBT.tikz(tree, with_env=True))