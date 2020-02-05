from magma import RS34

for m in range(1,6):
  print('norm:', m)
  print('---------------------------')
  for path in RS34.products(m):
    print(RS34.to_ascii(path))