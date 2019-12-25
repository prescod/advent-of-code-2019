from collections import defaultdict
import itertools
from typing import Sequence, Iterator

from intcomputer import Computer


program = [int(x) for x in open("day7.txt").read().split(",")]


def compute(inputs: Iterator):
    working_memory = defaultdict(int, enumerate(program))

    c = Computer(working_memory, inputs)
    return next(c.compute())


def test_settings(phase_settings: Sequence):
    assert len(phase_settings) == 5
    input = 0
    for i in range(0, 5):
        input = compute(iter([phase_settings[i], input]))
    return input


def test_permutations():
    mx = 0

    for permutation in itertools.permutations(range(0, 5)):
        rc = test_settings(permutation)
        mx = max(rc, mx)
    return mx


print(test_permutations())
