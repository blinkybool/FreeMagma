from magma import Catalan

class TwoRowTableaux(Catalan):
  """
  Standard Young Tableaux of shape (n-1,n-1) 
  Data Type: tuple(tuple(int))
  Format: a pair of sequences of positive integers
  Generator: ((),())
  Example: (n=5) ((1,2,3,7),(4,5,6,8))
    +-+-+-+-+
    |1|2|3|7|
    +-+-+-+-+
    |4|5|6|8|
    +-+-+-+-+
  """
  generator = lambda: ((),())

  @classmethod
  def product(cls, fst, snd):
    fst_top, fst_bot = fst
    snd_top, snd_bot = snd
    fst_size = len(fst_top) * 2
    snd_size = len(snd_top) * 2
    top = fst_top + (fst_size+1,) + tuple(x+fst_size+1 for x in snd_top)
    bot = fst_bot + tuple(x+fst_size+1 for x in snd_bot) + (fst_size+snd_size+2,)
    return (top, bot)

  @classmethod
  def to_ascii(cls, tableaux):
    if tableaux == cls.generator():
      return '+\n|\n+\n|\n+'
    num_cols = len(tableaux[0])
    max_digits = len(str(num_cols*2))

    row_sep = ('+' + '-' * max_digits) * num_cols + '+'

    ascii_table = row_sep
    for row in tableaux:
      ascii_table += '\n|' + '|'.join(f'{x:<{max_digits}}' for x in row) + '|\n' +  row_sep
    
    return ascii_table
