class Catalan:
  """
  Base class for all catalan structures. By default this class provides the
    'Cartesian Magma' Catalan structure.

  Subclass Specification:
    A Catalan subclass must specify a 0-input 'generator' function, a 2-input
    'product' function and a 1-input 'factorise' function. lambda expressions
    are recommended for simple functions.
    
  Cartesian Magma:
    An object in the cartesian magma is either the generator () (empty tuple),
    or an ordered pair of cartesian magma objects. A cartesian magma object has
    norm 1 if its the generator, otherwise its norm is the sum of the norms of 
    its two subobjects.
  Data Type: tuple(tuple(...)) (recursive)
  Format: () or a tuple-pair of Cartesian Magma objects
  Generator: ()
  Example: (m=5) (((),((),())),((),()))
  """
  generator = lambda: ()
  product = lambda fst, snd: (fst, snd)
  factorise = lambda arg: arg
  
  norm_cache = {}

  @classmethod
  def get_bijection(cls, Target_Catalan):
    def bijection(domain_elt):
      if domain_elt == cls.generator():
        return Target_Catalan.generator()
      else:
        fst, snd = cls.factorise(domain_elt)
        return Target_Catalan.product(_bijection(fst), bijection(snd))
    return bijection

  @classmethod
  def identity(cls):
    return cls.bijection(cls)

  @classmethod
  def products(cls, norm):
    if norm in cls.norm_cache: return cls.norm_cache[norm]

    cls.norm_cache[norm] = list(
      cls.product(fst, snd)
        for i in range(1,norm)
        for fst in cls.products(i)
        for snd in cls.products(norm - i)
    )
    return cls.norm_cache[norm]

  @classmethod
  def init_norm_cache(cls):
    cls.norm_cache = {1: [cls.generator()]}

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
    return 1 if obj==cls.generator() else sum(map(cls.norm, cls.factorise(obj)))

  @classmethod
  def direct_norm(cls, obj):
    raise NotImplementedError

  @classmethod
  def all_catalan_families(cls):
    yield cls
    for family in cls.__subclasses__():
      yield from family.all_catalan_families()