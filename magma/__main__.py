from magma import Catalan, PrefixStrings, PostfixStrings, InfixStrings, PlaneTrees, NonCrossingChords, Arches, Triangulations, CBTs, DyckPaths

# for postfix in InfixStrings.products(4):
#   fst, snd = InfixStrings.factorise(postfix)
#   print(postfix, InfixStrings.product(fst, snd))


# for n in range(1,5):
#   print(n)
#   print('\\vspace{0.5in}')
#   for obj in DyckPaths.products(n):
#     print(DyckPaths.tikz_command(obj, with_env=True))
#   print()

for fam in Catalan.all_catalan_families():
  print(fam.__name__)
  print(len(set(fam.products(5))))
  for obj in fam.products(5):
    print(fam.to_ascii(obj))