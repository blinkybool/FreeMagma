from magma import Catalan, PrefixStrings, PostfixStrings, InfixStrings, PlaneTrees, NonCrossingChords, Arches, Triangulations, CBTs, DyckPaths, FriezePatterns

# for postfix in InfixStrings.products(4):
#   fst, snd = InfixStrings.factorise(postfix)
#   print(postfix, InfixStrings.product(fst, snd))


for n in range(11,12):
  # print(n)
  # print('\\vspace{0.5in}')
  print('size:', n)
  for obj in FriezePatterns.products(n):
    print(FriezePatterns.to_ascii(obj))
  print()

# for fam in Catalan.all_catalan_families():
#   print(fam.__name__)
#   print(len(set(fam.products(5))))
#   for obj in fam.products(5):
#     print(fam.to_ascii(obj))

# print(FriezePatterns.to_ascii((2,2,1,5,1,3,1,3)))