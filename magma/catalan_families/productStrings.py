from magma import Catalan

class PrefixStrings(Catalan):
  """
  Prefix notation product strings of length 2m-1 representing products in a free
    magma on one generator, denoted by the symbol 'o', with a binary product '*'
  
  Data Type:
    String
  Format:
    words in the alphabet {*,o} where a valid prefix string is either a
    single 'o', or a '*' followed by two valid prefix strings.
  Generator:
    'o'
  Example: (m=5)
    '*o**oo*oo'
    this is the product of 'o' with '**oo*oo'
  """
  ID = 'MA2'
  names = ['Prefix Product Strings', 'Prefix Strings']
  keyword = {'string', 'prefix', '*', 'o', 'product', 'free', 'magma'}
  
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

  @classmethod
  def direct_norm(cls, prefix_string):
    return prefix_string.count('o')

class InfixStrings(Catalan):
  """
  Infix notation product strings of length 3m-2 representing products in a free 
    magma on one generator, denoted by the symbol 'o', with a binary product
    represented by juxtaposition.
  
  Data Type:
    String
  Format:
    words in the alphabet {*,(,)} where a valid infix string is either a
    single 'o', or two valid infix strings surrounded by a pair of '()'
  Generator:
    'o'
  Example: (m=5)
    '(o((oo)(oo)))'
    this is the product of 'o' with '((oo)(oo))'
  """
  ID = 'MA3'
  names = ['Infix Product Strings', 'Infix Strings']
  keyword = {'string', 'infix', '*', '(', ')', '()', 'product', 'free', 'magma'}

  generator = lambda: 'o'
  product = lambda fst, snd: '(' + fst + snd + ')'

  @classmethod
  def factorise(cls, infix_string):
    assert len(infix_string) >= 4
    assert infix_string[0] == '('
    assert infix_string[-1] == ')'

    balance = 0
    iterator = enumerate(infix_string)
    next(iterator)
    for i, char in iterator:
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

  @classmethod
  def direct_norm(cls, infix_string):
    return infix_string.count('o')

class PostfixStrings(PrefixStrings):
  """
  Postfix notation product strings of length 2m-1  representing products in a free
    magma on one generator, denoted by the symbol 'o', with a binary product '*'
  
  Data Type:
    String
  Format:
    words in the alphabet {*,o} where a valid postfix string is either a
    single 'o', or two valid postfix strings followed by a '*'.
  Generator:
    'o'
  Example: (m=5)
    'ooo*oo***'
    this is the product of 'o' with 'oo*oo**'
  """
  ID = 'MA4'
  names = ['Postfix Product Strings', 'Postfix Strings']
  keyword = {'string', 'postfix', '*', 'o', 'product', 'free', 'magma'}

  generator = lambda: 'o'
  product = lambda fst, snd: fst + snd + '*'

  @classmethod
  def factorise(cls, postfix_string):
    assert len(postfix_string) >= 3
    assert postfix_string[-1] == '*'

    return tuple(prefix_string[::-1] for prefix_string in reversed(super().factorise(postfix_string[::-1])))

  @classmethod
  def direct_norm(cls, postfix_string):
    return postfix_string.count('o')
