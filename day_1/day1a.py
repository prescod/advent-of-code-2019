lines = open("input.txt")


def fuel(x):
    return x // 3 - 2


print(sum(fuel(int(x)) for x in lines))
