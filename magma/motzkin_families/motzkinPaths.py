from magma import Motzkin

class MotzkinPaths(Motzkin):
  generator = lambda: ''
  unary = lambda path: path + 'R'
  binary = lambda fst, snd: fst + 'U' + snd + 'D'
  
  @classmethod
  def factorise(cls, motzkin_path):
    if motzkin_path[-1] == 'R':
      return motzkin_path[:-1]
    else:
      assert len(motzkin_path) >= 2
      assert motzkin_path[-1] == 'D'

      height = 0
      split = len(motzkin_path) - 1
      for step in reversed(motzkin_path):
        height += {'U': -1, 'D': 1, 'R': 0}[step]
        if height <= 0:
          return (motzkin_path[0:split], motzkin_path[split+1:-1])
        split -= 1
      else:
        raise ValueError
      