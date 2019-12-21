from collections import defaultdict
import itertools

from intcomputer import Computer


program = [int(x) for x in open("day7.txt").read().split(",")]
# program = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
#            27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5]
# program = [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54,
#            -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4,
#            53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10]


def start_computation(inputs):
    working_memory = defaultdict(int, enumerate(program))

    c = Computer(working_memory, inputs)
    return c.compute()


class Inputter:
    previous_inputter = None

    def __init__(self,):
        self._next_value = None

    def next_value(self):
        while 1:
            yield self._next_value


def test_settings(phase_settings):
    assert len(phase_settings) == 5
    num_computers = len(phase_settings)
    computations = []
    inputters = [Inputter() for i in range(num_computers)]
    previous_output = 0
    for i in range(num_computers):
        inputter = inputters[i]
        computation = start_computation(itertools.chain(
            [phase_settings[i], previous_output], inputter.next_value()))
        computations.append(computation)
        previous_output = next(computation)
        inputters[(i+1) % num_computers]._next_value = previous_output

    while 1:
        for i in range(num_computers):
            print(i)
            output = next(computations[i], None)
            if output is None:
                return previous_output
            previous_output = output
            inputters[(i+1) % num_computers]._next_value = previous_output

    return previous_output


def test_permutations():
    mx = 0

    for permutation in itertools.permutations(range(5, 10)):
        rc = test_settings(permutation)
        mx = max(rc, mx)
        print(permutation, rc, mx)
    return mx


print(test_permutations())
