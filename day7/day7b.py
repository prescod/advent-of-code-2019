from collections import defaultdict
import itertools

from intcomputer import Computer


program = [int(x) for x in open("day7.txt").read().split(",")]


def start_computation(inputs):
    working_memory = defaultdict(int, enumerate(program))

    c = Computer(working_memory, inputs)
    return c.compute()   # runs a bit and then waits for input


class Inputter:
    """Very thin abstraction over list for readability and debugging"""

    def __init__(self, identifier):
        self.identifier = identifier
        # self.values = [None]
        self.values = []

    def receiver(self):
        while 1:
            value = self.values.pop(0)
            # print("Reading", self.identifier, value)
            yield value

    def send(self, value):
        # print("Writing", self.identifier, 1)
        self.values.append(value)


def test_settings(phase_settings):
    assert len(phase_settings) == 5  # check for off-by-one errors!
    num_computers = len(phase_settings)
    computations = []  # will be a list of ongoing computations
    input_streams = [Inputter(i) for i in range(num_computers)]

    # queue up phase settings to test
    for i in range(num_computers):
        input_streams[i].send(phase_settings[i])

    # queue up starting value
    input_streams[0].send(0)

    # initialize all of the computers
    for i in range(num_computers):
        inputter = input_streams[i]
        computation = start_computation(input_streams[i].receiver())
        computations.append(computation)
        previous_output = next(computation)
        input_streams[(i+1) % num_computers].send(previous_output)

    # feedback until one of them exits
    while 1:
        for i, computation in enumerate(computations):
            output = next(computation, None)  # get the next output
            if output is None:
                return previous_output
            previous_output = output
            # send it to the next computation in the list
            input_streams[(i+1) % num_computers].send(previous_output)

    return previous_output


def test_permutations():
    mx = 0

    for permutation in itertools.permutations(range(5, 10)):
        rc = test_settings(permutation)
        mx = max(rc, mx)
        if mx == rc:
            print(permutation, rc)
    return mx


print(test_permutations())
