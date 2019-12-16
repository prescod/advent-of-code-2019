lines = open("input.txt")


def fuel(x):
    return x // 3 - 2


def meta_fuel(x):
    f = 0
    addition_fuel = fuel(x)

    while addition_fuel > 0:
        f += addition_fuel
        addition_fuel = fuel(addition_fuel)

    return f


print(meta_fuel(100756))

print(sum(meta_fuel(int(x)) for x in lines))
