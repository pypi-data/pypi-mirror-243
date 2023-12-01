import typing

"""
# * int() = 0
# * ~int() == -1 ->
# * -~int() = 1
"""


def power_find(n: int) -> typing.Generator[int, None, None]:
    """
    Generator over powers of two, something like:
    [1, 0, 0, 1]
    """
    for x in range(len(binary := bin(n)[:1:-1])):
        if int(binary[x]):
            yield x


def int_to_eso(n: int, eso_num: bool = True, eso_oper: bool = True) -> str:
    """
    The funny
    """
    if n < 0:
        sign = "-"
        n = abs(n)
    else:
        sign = ""
    powers = power_find(n=n)  # * Create a list with all the powers of 2 that are needed to get the number
    buffer = []  # * Create an empty list
    for power in powers:
        if eso_num:  # * -~int();
            if eso_oper:  # * .__add__ , .__pow__
                if power == 0:  # * Use int() instead of -~int() for 0 power (even/odd number)
                    buffer.append("(-~int().__add__(-~int())).__pow__(int())")
                else:
                    buffer.append(f"((-~int().__add__(-~int())).__pow__(-~int(){''.join(['.__add__(-~int())' for _ in range(power-1)])}))")
            else:  # * + , **
                if power == 0:
                    buffer.append("(-~int()+-~int())**(int())")
                else:
                    buffer.append(f"(-~int()+-~int())**(-~int(){''.join(['+-~int()' for _ in range(power-1)])})")
        else:  # * 2 , {pow}
            if eso_oper:
                buffer.append(f"((2).__pow__({power}))")
            else:
                buffer.append(f"(2**{power})")
    if eso_oper:
        monster = buffer[0]
        for i in buffer[1:]:
            monster += f".__add__({i})"
    else:
        monster = buffer[0]
        for i in buffer[1:]:
            monster += f"|({i})"
    return f"{sign}({monster})"
