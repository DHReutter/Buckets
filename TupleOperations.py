def t_mul(t1, i):
    return t1[0] * i, t1[1] * i


def tt_mul(t1, t2):
    return t1[0] * t2[0], t1[1] * t2[1]


def t_sub(t1, i):
    return t1[0] - i, t1[1] - i


def tt_sub(t1, t2):
    return t1[0] - t2[0], t1[1] - t2[1]
