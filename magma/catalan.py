#!/usr/bin/env python3

class Catalan:
  generator = lambda: ()
  product = lambda fst, snd: (fst, snd)
  factorise = lambda arg: arg
  
  norm_cache = {}

  @classmethod
  def bijection(cls, Target_Catalan):
    def _bijection(domain_elt):
      if domain_elt == cls.generator():
        return Target_Catalan.generator()
      else:
        fst, snd = cls.factorise(domain_elt)
        return Target_Catalan.product(_bijection(fst), _bijection(snd))
    return _bijection

  @classmethod
  def identity(cls):
    return cls.bijection(cls)

  @classmethod
  def products(cls, n):
    if n in cls.norm_cache: return cls.norm_cache[n]

    cls.norm_cache[n] = list(
      cls.product(fst, snd)
        for i in range(1,n)
        for fst in cls.products(i)
        for snd in cls.products(n - i)
    )
    return cls.norm_cache[n]

  @classmethod
  def init_norm_cache(cls):
    cls.norm_cache = {1: [cls.generator()]}

  @classmethod
  def to_ascii(cls, obj):
    return str(obj)

  @classmethod
  def norm(cls, obj):
    return 1 if obj==cls.generator() else sum(map(cls.norm, cls.factorise(obj)))

  @classmethod
  def all_catalan_families(cls):
    yield cls
    for family in cls.__subclasses__():
      yield from family.all_catalan_families()