from magma import RS115, RS1, TwoThreeOneAvoiding
# m = 5
# for perm in RS115.products(m):
#   print('--------------------------')
#   print(perm)
#   # print(RS115.to_ascii(perm))
#   if m > 1:
#     fst, snd = RS115.exhaustive_factorise(perm)
#     # print('exhaustve')
#     # print('fst:')
#     print(fst)
#     # print(RS115.to_ascii(fst))
#     # print('snd:')
#     print(snd)
#     # print(RS115.to_ascii(snd))

#     fst, snd = RS115.factorise(perm)
#     # print('factorise')
#     # print('fst:')
#     print(fst)
#     # print(RS115.to_ascii(fst))
#     # print('snd:')
#     print(snd)
#     # print(RS115.to_ascii(snd))

# perm = (2,1,3,5,4)
# print(RS115.to_ascii(perm))
# fst, snd = RS115.exhaustive_factorise(perm)
# print('exhaustive')
# print('fst:')
# print(RS115.to_ascii(fst))
# print('snd:')
# print(RS115.to_ascii(snd))

# fst, snd = RS115.factorise(perm)
# print('factorise')
# print('fst:')
# print(RS115.to_ascii(fst))
# print('snd:')
# print(RS115.to_ascii(snd))

perm1 = ()
perm2 = (2,1,3)

perm = TwoThreeOneAvoiding.product(perm1, perm2)
fact_perm = TwoThreeOneAvoiding.factorise(perm)

print(perm1)
print(perm2)
print(perm)
print(fact_perm)