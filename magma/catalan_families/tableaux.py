from magma import Catalan

class RS168(Catalan):
  """
  Standard Young Tableaux of shape (m-1,m-1) 
  
  Data Type:
    tuple(tuple(int))
  Format:
    a pair of sequences of positive integers
  Generator:
    ((),())
  Example: (m=5)
    ((1,2,3,7),(4,5,6,8))
    +-+-+-+-+
    |1|2|3|7|
    +-+-+-+-+
    |4|5|6|8|
    +-+-+-+-+
  """
  ID='RS168'
  names = ['Two Row Standard Young Tableaux']
  keywords = {'two', 'row', 'standard', 'young', 'tableaux', 'table', 'sequence'}

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
  def factorise(cls, tableaux):
    top, bot = tableaux
    for i in reversed(range(len(top))):
      if i==0 or bot[i-1] + 1 == top[i]:
        break
    
    fst = (top[:i], bot[:i])
    shift = lambda x: x - 2 * len(fst[0]) - 1
    snd = (tuple(map(shift, top[i+1:])), tuple(map(shift, bot[i:-1])))
    return (fst, snd)

  @classmethod
  def direct_norm(cls, tableaux):
    return len(tableaux[0])+1

  @classmethod
  def to_ascii(cls, tableaux):
    # if tableaux == cls.generator():
    #   return '+\n|\n+\n|\n+'
    num_cols = len(tableaux[0])
    max_digits = len(str(num_cols*2))

    row_sep = ('+' + '-' * max_digits) * num_cols + '+'

    ascii_table = row_sep
    for row in tableaux:
      ascii_table += '\n|' + ''.join(f'{x:<{max_digits}}|' for x in row) + '\n' +  row_sep
    
    return ascii_table