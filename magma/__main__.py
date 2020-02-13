from magma import RS57 as SP, RS1 as Tri, RS5 as CBT, RS61 as Arch

def poster_triangulations():
  for m in range(1,5):
    for tri in Tri.products(m):
      print('{', Tri.tikz_command(tri, with_env=False, colour_factors=True), '}')

def poster_SP():
  for m in range(1,5):
    for poly in SP.products(m):
      # print(SP.tikz(poly, with_env=True, colour_factors=True))
      print('{\n  ' + SP.tikz(poly, with_env=False, colour_factors=True).replace('\n', '  \n') + '\n}')

def poster_CBT():
  for m in range(1,5):
    for cbt in CBT.products(m):
      print('{', CBT.tikz_command(cbt, with_env=True, colour_factors=True), '}')

def poster_Arches():
  for m in range(1,5):
    for matching in Arch.products(m):
      print('{', Arch.tikz_command(matching, with_env=False, colour_factors=True),'}')


# poster_triangulations()

# # poly = ('NNNEENNEE', 'EENNEENNN')
# # print(SP.tikz(poly, colour_factors=True))

poster_SP()

# m=8

# big_poly = ('NENENNEE', 'EENENENN')
# big_cbt = SP.get_bijection(CBT)(big_poly)
# big_arch = SP.get_bijection(Arch)(big_poly)
# big_tri = SP.get_bijection(Tri)(big_poly)

# print(SP.tikz(big_poly, colour_factors=True))
# print(Arch.tikz_command(big_arch, colour_factors=True))
# print(Tri.tikz_command(big_tri, colour_factors=True))
# print(CBT.tikz_command(big_cbt, colour_factors=True))

# for poly in SP.products(m):
#   print(poly)
#   print(SP.tikz(poly, with_env=True, colour_factors=True))
#   print()