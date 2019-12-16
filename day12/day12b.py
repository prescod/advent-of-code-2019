from dataclasses import dataclass
from copy import deepcopy


@dataclass
class Vector:
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)


def cmp(a, b):
    """https://codegolf.stackexchange.com/questions/49778/how-can-i-use-cmpa-b-with-python3"""
    return (a > b) - (a < b)


@dataclass
class Moon:
    pos: Vector = Vector(0, 0, 0)
    velocity: Vector = Vector(0, 0, 0)

    def __init__(self, pos):
        self.pos = pos

    def update_velocities(self, other: "Moon"):
        v_delta = Vector(
            cmp(other.pos.x, self.pos.x),
            cmp(other.pos.y, self.pos.y),
            cmp(other.pos.z, self.pos.z),
        )
        self.velocity += v_delta

    def update_position(self):
        self.pos += self.velocity


def simulate(steps: int, moons: list):
    # first_state = deepcopy(moon.pos for moon in moons)
    # assert first_state == moons
    for i in range(steps):
        for m1 in moons:
            for m2 in moons:
                m1.update_velocities(m2)

        for m in moons:
            m.update_position()
        print(moons[1].velocity.y, end=" ")
        # if first_state == moons:
        #     print(i)
        #     assert 0, i


moons = [
    Moon(Vector(-1, 0, 2)),
    Moon(Vector(2, -10, -7)),
    Moon(Vector(4, -8, 8)),
    Moon(Vector(3, 5, -1)),
]

simulate(3000, moons)
