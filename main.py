import operator
from functools import reduce
from itertools import permutations, batched

import click

OPS = [operator.sub, operator.truediv, operator.mul]


def is_numeric_core(number: float) -> bool:
    return number.is_integer() and number > 0 and len(str(abs(number))) <= 4


def do_op(left, op, right):
    return op(left, right)


def numeric_core(numbers: list[int]):
    if len(numbers) != 4:
        raise ValueError("Numbers must be four!")

    operations = permutations(OPS)
    results = []
    for op_group in operations:
        res = reduce(lambda acc, current: do_op(acc, *current), zip(op_group, numbers[1:]), numbers[0])
        results.append(res)

    return filter(is_numeric_core, results)


def word_core(word: str):
    if len(word) > 4:
        raise ValueError("Only four letter words are supported!")

    as_numbers = map(lambda char: ord(char.lower()) - ord('a') + 1, word)
    core = numeric_core(list(as_numbers))
    return word, list(core)


def number_as_letter(number):
    return chr(int(number) + 96)


def core_to_letter(core):
    filtered_cores = list(filter(lambda x: 0 <= x <= 26, core[1]))
    return number_as_letter(min(filtered_cores)) if len(filtered_cores) > 0 else 'N/A'


def tabulate(cores, cols=5):
    rows = batched(cores, cols)

    for row in rows:
        header = [r[0] for r in row]
        content = [core_to_letter(r) for r in row]
        print(header)
        print(content)


@click.command()
@click.option("--numbers", "-n", nargs=4, default=[None, None, None, None], type=click.INT,
              help="Calculate the numeric core of 4 numbers")
@click.option("--words", "-w", multiple=True, default=[], help="Calculate the numeric core of a list of words")
@click.option("--table", default=False, flag_value="table", help="Display words cores as table")
def main(numbers, words, table):
    if all(numbers):
        cores = numbers, list(numeric_core(numbers))
        print(cores)
    if len(words) > 1:
        cores = list(map(word_core, words))
        if table:
            tabulate(cores)
            return


if __name__ == '__main__':
    main()
