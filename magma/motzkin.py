class Motzkin:
  """
  Base class for all Motzkin structures. By default this class provides the
    'Cartesian Magma' Motzkin structure.

  Subclass Specification:
    A Motzkin subclass must specify a 0-input 'generator' function, a 1-input
    'unary' function, a 2-input 'binary' function and a 1-input 'factorise'
    function. lambda expressions are recommended for simple functions.
    
  Cartesian Motzkin Magma:
    An object in the cartesian Motzkin magma is either the generator () (empty tuple),
    a singleton tuple of an object or a pair of objects.
  Data Type:
    tuple(tuple(...)) (recursive)
  Format:
    Object := () | (Object,) | (Object, Object)
  """
  
  ID = 'MMA1'
  names = ['Cartesian Motzkin Free Magma']
  keywords = {'motkzin', 'cartesian', 'free', 'magma', 'tuple'}

  generator = lambda: ()
  unary = lambda obj: (obj,)
  binary = lambda fst, snd: (fst, snd)
  factorise = lambda obj: obj
  
  norm_cache = {}

  @classmethod
  def get_bijection(cls, Target_Motzkin):
    def bijection(obj):
      if obj == cls.generator():
        return Target_Motzkin.generator()
      else:
        factors = tuple(map(bijection, cls.factorise(obj)))
        return {1: Target_Motzkin.unary, 2: Target_Motzkin.binary}[len(factors)](factors)
    return bijection

  @classmethod
  def identity(cls):
    return cls.get_bijection(cls)

  @classmethod
  def products(cls, norm):
    if norm in cls.norm_cache: return cls.norm_cache[norm]
    
    cls.norm_cache[norm] = [cls.unary(obj) for obj in cls.norm_cache[norm-1]]

    cls.norm_cache[norm].extend(
      cls.binary(fst, snd)
        for i in range(1,norm-1)
        for fst in cls.products(i)
        for snd in cls.products(norm - i - 1)
    )
    return cls.norm_cache[norm]

  @classmethod
  def init_caches(cls):
    cls.norm_cache = {1: [cls.generator()], 2: [cls.unary(cls.generator())]}

  @classmethod
  def verify(cls, obj):
    if obj == cls.generator(): return True

    try:
      return all(map(cls.verify, cls.factorise(obj)))
    except:
      return False
    
  @classmethod
  def normalise(cls, obj):
    return obj

  @classmethod
  def equal(cls, a, b):
    return cls.normalise(a) == cls.normalise(b)

  @classmethod
  def to_ascii(cls, obj):
    return str(obj)

  @classmethod
  def norm(cls, obj):
    return 1 if obj==cls.generator() else 1 + sum(map(cls.norm, cls.factorise(obj)))

  @classmethod
  def direct_norm(cls, obj):
    raise NotImplementedError

  @classmethod
  def iter_families(cls):
    yield cls
    for family in cls.__subclasses__():
      yield from family.iter_families()