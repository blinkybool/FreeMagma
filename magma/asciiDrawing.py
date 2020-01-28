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