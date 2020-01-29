from magma import Catalan

class PrefixStrings(Catalan):
  generator = lambda: 'o'
  product = lambda fst, snd: '*' + fst + snd

  @classmethod
  def factorise(cls, prefix_string):
    assert len(prefix_string) >= 3
    assert prefix_string[0] == '*'

    # stack keeps track of how many arguments still need to be read for the
    # '*' symbols read so far (one of 2,1,0)
    stack = []
    for i, char in enumerate(prefix_string):
      if char == '*':
        stack.append(2)
      else:
        assert char == 'o'
        stack[-1] -= 1
      
      while stack[-1] == 0:
        stack.pop()
        stack[-1] -= 1
      
      # split between the arguments of the outermost * has been found
      if stack[0] <= 1:
        split = i+1
        break
    else:
      raise ValueError

    return (prefix_string[1:split], prefix_string[split:])

class InfixStrings(Catalan):
  generator = lambda: 'o'
  product = lambda fst, snd: '(' + fst + snd + ')'

  @classmethod
  def factorise(cls, infix_string):
    assert len(infix_string) >= 4
    assert infix_string[0] == '('
    assert infix_string[-1] == ')'

    balance = 0
    for i, char in enumerate(infix_string[1:]):
      if char == '(':
        balance += 1
      elif char == ')':
        balance -= 1
      else:
        assert char == 'o'
      
      if balance == 0:
        split = i + 1
        break
    else:
      raise ValueError

    return (infix_string[1:split], infix_string[split:-1])

class PostfixStrings(Catalan):
  generator = lambda: 'o'
  product = lambda fst, snd: fst + snd + '*'

  @classmethod
  def factorise(cls, postfix_string):
    assert len(postfix_string) >= 3
    assert postfix_string[-1] == '*'

    return tuple(prefix_string[::-1] for prefix_string in reversed(PrefixStrings.factorise(postfix_string[::-1])))


