class FreeMagma {

	static factorise(_) {
		throw new Error('factorise method not implemented!');
	}

	static product({ funcID, args }) {
		return this.operators[args.length][funcID](...args);
	}

	static converter(Domain, Codomain) {
		return (x) => Codomain.product(Domain.factorise(x));
	}

	static identity = (Domain) => this.converter(Domain, Domain);
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

	static infix_rep(magma_product) {
		if (magma_product.is_generator()) {
			return 'o'; 
		} else {
			let {args: [first, second]} = magma_product;
			return '(' + this.infix_rep(first) + '*' + this.infix_rep(second) + ')';
		}
	}

	static prefix_rep(magma_product) {
		if (magma_product.is_generator()) {
			return 'o'; 
		} else {
			let {args: [first, second]} = magma_product;
			return '*' + this.prefix_rep(first) + this.prefix_rep(second);
		}
	}

	static postfix_rep(magma_product) {
		if (magma_product.is_generator()) {
			return 'o'; 
		} else {
			let {args: [first, second]} = magma_product;
			return this.postfix_rep(first) + this.postfix_rep(second) + '*';
		}
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
	static binary_op_vert(first, second) {
		const separator = (first.is_generator() ? '' : '\n');

		return second.is_generator() ?
			Mountains.product(first) + separator + '\\\n/'
			: Mountains.product(first) + separator +
					'\\\n ' +
					Mountains.product(second).replace(/\n/g, '\n ') +
					'\n/';
	}
	static binary_op_hori = (first, second) => {
		const first_rows = this.product(first).split('\n');
		let second_rows = this.product(second).split('\n');

		if (second.is_generator()) {
			second_rows = [ '/\\' ];
		} else {
			second_rows = second_rows.map((currentValue) => ' ' + currentValue + ' ');
			second_rows.push('/' + ' '.repeat(second_rows[0].length - 2) + '\\');
		}

		const height = Math.max(first_rows.length, second_rows.length);

		for (let piece_rows of [first_rows, second_rows]) {
			const row_fill = ' '.repeat(piece_rows[0].length);
			const num_padding_rows = height - piece_rows.length
			piece_rows.unshift(...Array(num_padding_rows).fill(row_fill));
		}

		let result_rows = [];
		for (let i=0; i<height; ++i) {
			result_rows.push(first_rows[i] + second_rows[i]);
		}

		return result_rows.join('\n');
	}
	
	static operators = [ [ this.generator ], undefined, [ this.binary_op_hori ] ];

	static factorise(mountain) {
		if (mountain == '') return new UniqueGenerator();

		const rows = mountain.split('\n');

		const split_index = rows[rows.length-1].lastIndexOf('/');
		const first_rows = [];
		const second_rows = [];

		for (let row of rows) {
			first_rows.push(row.slice(0,split_index));
			second_rows.push(row.slice(split_index+1, row.length-1));
		}
		second_rows.pop();

		for (let piece_rows of [ first_rows, second_rows]) {
			// Remove whitespace rows
			while (piece_rows.length > 0 && /^\s*$/.test(piece_rows[0])) piece_rows.shift();
		}

		return new UniqueProduct(this.factorise(first_rows.join('\n')),
														 this.factorise(second_rows.join('\n')));
	}

	static factorise_vert(mountain) {
		if (mountain == '') return new UniqueGenerator();

		const last_off_diag = mountain.lastIndexOf('\n\\') + 1;
		const first = mountain.slice(0, last_off_diag);
		const second = mountain.slice(last_off_diag + 3, mountain.length - 1).replace(/\n /g, '\n');

		return new UniqueProduct(this.factorise(first), this.factorise(second));
	}
}

for (let i = 0; i <= 5; ++i) {
	console.log('Catalan Size: ' + i);
	console.log('----------------');
	for (let catalan_product of Catalan.catalan_products(i)) {
		let mountain = Mountains.product(catalan_product);
		// console.log(Mountains.product(Mountains.factorise(mountain)));
		console.log(mountain);
		console.log(Brackets.product(catalan_product));
		
		console.log('-'.repeat(i*2));
  }
}