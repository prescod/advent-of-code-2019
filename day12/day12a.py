from dataclasses import dataclass
from yaml import load


@dataclass
class Vector:
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def energy(self):
        return sum(abs(v) for v in [self.x, self.y, self.z])


def cmp(a, b):
    """https://codegolf.stackexchange.com/questions/49778/how-can-i-use-cmpa-b-with-python3"""
    return (a > b) - (a < b)


@dataclass
class Moon:
    pos: Vector = Vector(0, 0, 0)
    velocity: Vector = Vector(0, 0, 0)
    energy: int = 0

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
        self.energy = self.pos.energy() * self.velocity.energy()


def simulate(steps: int, moons: list):
    for _ in range(steps):
        for m1 in moons:
            for m2 in moons:
                m1.update_velocities(m2)

        for m in moons:
            m.update_position()

        print(sum(m.energy for m in moons), moons)


moons = [
    Moon(Vector(4, 12, 13)),
    Moon(Vector(-9, 14, -3)),
    Moon(Vector(-7, -1, 2)),
    Moon(Vector(-11, 17, -1)),
]

simulate(1000, moons)
