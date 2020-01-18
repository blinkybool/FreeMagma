class FreeMagma {
	constructor(signature) {
		this.signature = signature;
	}

	static factorise(_) {
		throw new Error('factorise method not implemented!');
	}

	static product({ funcID, args }) {
		return this.operators[args.length][funcID](...args);
	}
}

class MagmaProduct {
	constructor(funcID, ...args) {
		this.funcID = funcID;
		this.args = args;
		this.height = args.length > 0 ? Math.max(...args) : 0;
	}

	is_generator = () => this.args == 0;
}

class MagmaGenerator extends MagmaProduct {
	constructor(funcID) {
		super(funcID);
	}
}

class UniqueProduct extends MagmaProduct {
	constructor(...args) {
		super(0, ...args);
	}
}

class UniqueGenerator extends MagmaGenerator {
	constructor() {
		super(0);
	}
}

class Catalan extends FreeMagma {
  static signature = [1,undefined,1];

	static catalan_products(n) {
		let cache = [ [ new UniqueGenerator() ] ];

    for (let k=1; k<=n; ++k) {
      let magma_products = [];
      for (let i = 0; i < k; ++i) {
        for (let first of cache[i]) {
          for (let second of cache[k - i - 1]) {
            magma_products.push(new UniqueProduct(first, second));
          }
        }
      }
      cache[k] = magma_products
    }

		return cache[n];
	}

	static catalan_objects(n) {
		return this.catalan_products(n).map((currentValue) => this.product(currentValue));
	}
}

class Brackets extends Catalan {
	static generator = () => '';
	static binary_op = (first, second) => Brackets.product(first) + '(' + Brackets.product(second) + ')';
	static operators = [ [ this.generator ], undefined, [ this.binary_op ] ];

	static factorise(brackets) {
		if (brackets == '') return new UniqueGenerator();

		let unpaired = 1;
		let i = brackets.length - 1;
		while (unpaired > 0 && --i >= 0) {
			if (brackets[i] == '(') {
				--unpaired;
			} else if (brackets[i] == ')') {
				++unpaired;
			}
		}
		let first = this.factorise(brackets.slice(0, i));
		let second = this.factorise(brackets.slice(i + 1, -1));
		return new UniqueProduct(first, second);
	}
}

class Mountains extends Catalan {
	static generator = () => '';
	static binary_op(first, second) {
		const separator = (first.is_generator() ? '' : '\n');

		return second.is_generator()
			? Mountains.product(first) + separator + '\\\n/'
			: Mountains.product(first) + separator +
					'\\\n ' +
					Mountains.product(second).replace(/\n/g, '\n ') +
					'\n/';
	}
	static operators = [ [ this.generator ], undefined, [ this.binary_op ] ];

	static factorise(mountain) {
		if (mountain == '') return new UniqueGenerator();

		const last_off_diag = mountain.lastIndexOf('\n\\') + 1;
		const first = mountain.slice(0, last_off_diag);
		const second = mountain.slice(last_off_diag + 3, mountain.length - 1).replace(/\n /g, '\n');

		return new UniqueProduct(this.factorise(first), this.factorise(second));
	}
}

for (i = 0; i <= 5; ++i) {
	console.log('Catalan Size: ' + i);
	console.log('----------------');
	for (let catalan_product of Catalan.catalan_products(i)) {
		console.log(Brackets.product(catalan_product));
		console.log(Mountains.product(catalan_product));
  }
}

