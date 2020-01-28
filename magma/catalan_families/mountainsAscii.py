from magma import Catalan

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