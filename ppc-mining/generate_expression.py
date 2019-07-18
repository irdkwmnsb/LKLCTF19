import random


# Mean of normal distribution
MU = 20.0
# Variance of normal distribution
SIGMA = 10.0
# Minimal complexity
MIN = 5


class Node:
    pass


class Terminal(Node):
    def __init__(self, value, parent):
        self.value = value

        # Я очень надесь, что эта циклическая ссылка не создаст проблем для сборщика мусора.
        # Если создаст, то нужно будет заменить на хреньку из модуля weakref
        self.parent = parent

    def fmt(self, prio):
        del prio
        #if self.value < 0:
        #    return f'({self.value})'
        return str(self.value)


def getprio(op):
    return {
        '+': 100,
        '-': 100,
        '*': 500,
        '/': 500,
    }[op]


class Binop(Node):
    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs
        lhs.parent = self
        rhs.parent = self

    def replace(self, old, new):
        if old is self.lhs:
            self.lhs = new
        elif old is self.rhs:
            self.rhs = new
        else:
            raise Exception('Logical error: Binop had no node with such id')

    def fmt(self, prio=-1000):
        p = getprio(self.op)
        if p <= prio:
            return f'({self.lhs.fmt(p)} {self.op} {self.rhs.fmt(p)})'
        else:
            return f'{self.lhs.fmt(p)} {self.op} {self.rhs.fmt(p)}'


def make_add(value):
    x = random.randint(-1000, 1000)
    return x, value - x


def make_sub(value):
    x = random.randint(-1000, 1000)
    return value + x, x


def factor(value):
    ok = 1
    x = 1
    while x * x <= value:
        if value % x == 0:
            ok = x
            # No break
        x += 1
    return ok, value // ok


def make_mul(value):
    return factor(value)


def make_div(value):
    x = random.randint(-1000, 1000)
    return value * x, x


def make_random_binop(term):
    assert isinstance(term, Terminal)
    op = random.choice('+-*/')
    lhs, rhs = {
        '+': make_add,
        '-': make_sub,
        '*': make_mul,
        '/': make_div,
    }[op](term.value)

    return Binop(op, Terminal(lhs, None), Terminal(rhs, None))


def gen_expression(result):
    n = round(random.gauss(MU, SIGMA))
    assert type(n) is int

    root = Terminal(result, None)
    terminals = [root]
    for i in range(max(n, MIN)):
        node = random.choice(terminals)
        new = make_random_binop(node)
        if node is root:
            root = new
        terminals.remove(node)
        if node.parent is not None:
            node.parent.replace(node, new)
        terminals += [new.lhs, new.rhs]
    return root.fmt()
