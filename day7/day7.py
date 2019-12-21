from collections import defaultdict
import itertools

from intcomputer import Computer


program = [int(x) for x in open("day7.txt").read().split(",")]
# program = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
# # program = [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23,
# #            101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]
# program = [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33,
#            1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0]


def compute(inputs):
    working_memory = defaultdict(int, enumerate(program))

    class Output:
        def output(self, value):
            self.value = value

    output = Output()

    c = Computer(working_memory, inputs, output.output)
    c.compute()
    return output.value


def test_settings(phase_settings):
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
