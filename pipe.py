class Pipe:
    def __init__(self,*args):
        self.args = args
        self.computation = []

    def __rshift__(self, next_function):
        self.computation.append(next_function)
        return self

    def __call__(self,*args):
        g = self.computation.pop()(*self.args , *args)
        for f in self.computation:
            g = f(g)
        return g

    def __lshift__(self, other):
        #self.args = self.args + (other,) if len(self.args) > 0 else (other,)
        self.args = (*self.args,other)
        return self.__call__()

def due(args):
    return 2 * args

def square(x):
    return x**2
