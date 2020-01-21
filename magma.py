#!/usr/bin/env python3

class Catalan:
	generator = lambda: None
	binary_op = lambda *_: None

	@staticmethod
	def fmap(Domain, Codomain):
		return lambda x: Codomain.multiply(Domain.factorise(x))

	@classmethod
	def fmap_to(cls, Codomain):
		return cls.fmap(cls, Codomain)

	@classmethod
	def identity(cls):
		return cls.fmap(cls, cls)

	@classmethod
	def factorise(cls, cartesian):
		raise NotImplementedError()

	@classmethod
	def multiply(cls, cartesian):
		if cartesian in cls.multiply_cache:
			return cls.multiply_cache[cartesian]
		else:
			fst, snd = cartesian
			result = cls.multiply_cache[cartesian] = cls.binary_op(cls.multiply(fst), cls.multiply(snd))
			return result

class Cartesian(Catalan):
	generator = lambda: ()
	binary_op = lambda fst, snd: (fst, snd)

	@classmethod
	def factorise(cls, cartesian):
		return cartesian

	@classmethod
	def products(cls, n):
		if n in cls.generator_cache: return cls.generator_cache[n]

		cls.generator_cache[n] = list(cls.binary_op(fst, snd)
			for i in range(n)
				for fst in cls.products(i)
					for snd in cls.products(n - i - 1)
		)
		return cls.generator_cache[n]

class PrefixString(Catalan):
	generator = lambda: 'o'
	binary_op = lambda fst, snd: '*' + fst + snd

class InfixString(Catalan):
	generator = lambda: 'o'
	binary_op = lambda fst, snd: '(' + fst + '*' + snd + ')'

class PostfixString(Catalan):
	generator = lambda: 'o'
	binary_op = lambda fst, snd: fst + snd + '*'

class Brackets(Catalan):
	generator = lambda: ''
	binary_op = lambda fst, snd: fst + '{' + snd + '}'

	@classmethod
	def factorise(cls, brackets):
		if brackets == '': return Cartesian.generator()

		unpaired = 1
		for i in range(len(brackets) - 2, -1, -1):
			unpaired += 1 if brackets[i]=='}' else -1
			if unpaired <= 0: break
		
		fst = cls.factorise(brackets[0:i])
		snd = cls.factorise(brackets[i+1:-1])
		return Cartesian.binary_op(fst, snd)

class Mountains(Catalan):
	generator = lambda: ''
	binary_op = lambda *args: Mountains._binary_op(*args)

	@classmethod
	def _binary_op(cls, fst, snd):
		fst_rows = fst.split('\n')

		if snd == cls.generator():
			snd_rows = [ '/\\' ]
		else:
			snd_rows = [' ' + row + ' ' for row in snd.split('\n')]
			snd_rows.append('/' + ' ' * (len(snd_rows[0]) - 2) + '\\')

		height = max(len(fst_rows), len(snd_rows))

		fst_rows = [' ' * len(fst_rows[0])] * (height - len(fst_rows)) + fst_rows
		snd_rows = [' ' * len(snd_rows[0])] * (height - len(snd_rows)) + snd_rows

		return '\n'.join(fst_row + snd_row for fst_row, snd_row in zip(fst_rows, snd_rows))

	@classmethod
	def factorise(cls, mountain):
		if mountain == '': return Cartesian.generator()

		rows = mountain.split('\n')

		split_index = rows[-1].rfind('/')
		fst_rows = [row[0:split_index] for row in rows]
		snd_rows = [row[split_index+1:-1] for row in rows[:-1]]

		for piece_rows in fst_rows, snd_rows:
			# Remove whitespace rows
			while len(piece_rows) > 1 and (piece_rows[0].isspace() or piece_rows[0] == ''):
				piece_rows.pop(0)

		return Cartesian.binary_op(cls.factorise('\n'.join(fst_rows)),
												 			cls.factorise('\n'.join(snd_rows)))

for Catalan_Family in [Catalan] + Catalan.__subclasses__():
	Catalan_Family.generator_cache = {0: [Catalan_Family.generator()]}
	Catalan_Family.multiply_cache = {Cartesian.generator(): Catalan_Family.generator()}

if __name__ == "__main__":
	print(len(Cartesian.products(13)))
	for prod in Cartesian.products(13):
		Cartesian.fmap_to(Mountains)(prod)
		Cartesian.fmap_to(Brackets)(prod)