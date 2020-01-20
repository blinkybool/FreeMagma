from memorize import Memorize

class FreeMagma:

	@classmethod
	def factorise(cls, object):
		pass

	@classmethod
	def get_operators(cls):
		return dict()

	@classmethod
	def product(cls, magma_product):
		return cls.get_operators()[len(magma_product.args)][magma_product.funcID](*magma_product.args)

	@staticmethod
	def converter(Domain, Codomain):
		return lambda x: Codomain.product(Domain.factorise(x))

	@classmethod
	def identity(cls):
		assert cls != FreeMagma
		return cls.converter(cls, cls)

class MagmaProduct:
	def __init__(self, funcID, *args):
		self.funcID = funcID
		self.args = args
		self.height = max((arg.height + 1 for arg in args), default=0)
		self.rep = '({}{})'.format(funcID, ''.join(arg.rep for arg in args))

	def __eq__(self, value):
	 return type(self) == type(value) and self.rep == value.rep

	def __len__(self):
		return self.args.__len__()

	def is_generator(self):
		return len(self) == 0

class MagmaGenerator(MagmaProduct):
	def __init__(self, funcID):
		super().__init__(funcID)

class UniqueProduct(MagmaProduct):
	def __init__(self, *args):
	 super().__init__(0, *args)

class UniqueGenerator(MagmaGenerator):
	def __init__(self):
		super().__init__(0)

class Catalan(FreeMagma):

	GENERATOR_SYMBOL = 'o'
	PRODUCT_SYMBOL = '*'

	@classmethod
	def catalan_products(cls, n):
		@Memorize
		def _catalan_products(n):
			if n == 0: return [UniqueGenerator()]

			magma_products = []
			for i in range(n):
				for fst in _catalan_products(i):
					for snd in _catalan_products(n - i - 1):
						magma_products.append(UniqueProduct(fst, snd))

			return magma_products
		return _catalan_products(n)

	@classmethod
	def catalan_objects(cls, n):
		return list(map(cls.product, cls.catalan_products(n)))

	@classmethod
	def infix_rep(cls, magma_product):
		if magma_product.is_generator():
			return cls.GENERATOR_SYMBOL 
		else:
			fst, snd = magma_product.args
			return '(' + cls.infix_rep(fst) + cls.PRODUCT_SYMBOL + cls.infix_rep(snd) + ')'

	@classmethod
	def prefix_rep(cls, magma_product):
		if magma_product.is_generator():
			return cls.GENERATOR_SYMBOL 
		else:
			fst, snd = magma_product.args
			return cls.PRODUCT_SYMBOL + cls.prefix_rep(fst) + cls.prefix_rep(snd)

	@classmethod
	def postfix_rep(cls, magma_product):
		if magma_product.is_generator():
			return cls.GENERATOR_SYMBOL 
		else:
			fst, snd = magma_product.args
			return cls.postfix_rep(fst) + cls.postfix_rep(snd) + cls.PRODUCT_SYMBOL

class Brackets(Catalan):
	generator = lambda: ''
	binary_op = lambda fst, snd: Brackets.product(fst) + '(' + Brackets.product(snd) + ')'

	@classmethod
	def get_operators(cls):
		if 'operators' not in cls.__dict__:
			cls.operators = {0: [cls.generator], 2: [cls.binary_op]}
		return cls.operators

	@classmethod
	def factorise(cls, brackets):
		if brackets == '': return UniqueGenerator()

		unpaired = 1
		for i in range(len(brackets) - 2, -1, -1):
			unpaired += 1 if brackets[i]==')' else -1
			if unpaired <= 0: break
		
		fst = cls.factorise(brackets[0:i])
		snd = cls.factorise(brackets[i+1:-1])
		return UniqueProduct(fst, snd)

class Mountains(Catalan):

	generator = lambda: ''
	@classmethod
	def binary_op_vert(cls, fst, snd):
		separator = '' if fst.is_generator() else '\n'
		return cls.product(fst) + separator + '\\\n/' if snd.is_generator() else cls.product(fst) + separator + '\\\n ' + cls.product(snd).replace('\n', '\n ') + '\n/'

	@classmethod
	def binary_op_hori(cls, fst, snd):
		fst_rows = cls.product(fst).split('\n')

		if snd.is_generator():
			snd_rows = [ '/\\' ]
		else:
			snd_rows = [' ' + row + ' ' for row in cls.product(snd).split('\n')]
			snd_rows.append('/' + ' ' * (len(snd_rows[0]) - 2) + '\\')

		height = max(len(fst_rows), len(snd_rows))

		fst_rows = [' ' * len(fst_rows[0])] * (height - len(fst_rows)) + fst_rows
		snd_rows = [' ' * len(snd_rows[0])] * (height - len(snd_rows)) + snd_rows

		return '\n'.join(fst_row + snd_row for fst_row, snd_row in zip(fst_rows, snd_rows))

	@classmethod
	def get_operators(cls):
		if 'operators' not in cls.__dict__:
			cls.operators = {0: [cls.generator], 2: [cls.binary_op_hori]}
		return cls.operators

	@classmethod
	def factorise(cls, mountain):
		if mountain == '': return UniqueGenerator()

		rows = mountain.split('\n')

		split_index = rows[-1].rfind('/')
		fst_rows = [row[0:split_index] for row in rows]
		snd_rows = [row[split_index+1:-1] for row in rows[:-1]]

		for piece_rows in fst_rows, snd_rows:
			# Remove whitespace rows
			while len(piece_rows) > 1 and (piece_rows[0].isspace() or piece_rows[0] == ''):
				piece_rows.pop(0)

		return UniqueProduct(cls.factorise('\n'.join(fst_rows)),
												 cls.factorise('\n'.join(snd_rows)))

	@classmethod
	def factorise_vert(cls, mountain):
		if mountain == '': return UniqueGenerator()

		split_index = mountain.rfind('\n\\') + 1
		fst = mountain[0:split_index]
		snd = mountain[split_index + 3:-2].replace('\n ', '\n')

		return UniqueProduct(cls.factorise(fst), cls.factorise(snd))


if __name__ == "__main__":
	for i in range(12):
		print(f'Catalan Size: {i}')
		print('----------------')
		for catalan_product in Catalan.catalan_products(i):
			print(Mountains.product(catalan_product))
			print(Brackets.product(catalan_product))
			print('-'*i*2)
