class PlaceHolderArg:
    pass


class Pipe:
    def __init__(self,*args):
        """
        initialize the pipe by passing arguments for the first function.
        This is optional. Arguments passed here will be used
        """
        self.args = args
        self.computation = []

    def __rshift__(self, next_function):
        """Pipes a function. The will be executed in the order they are piped,
        left to right
         p = Pipe(a,b) >> f >> g >> h ---> h(g(f(a,b)))
        """
        self.computation.append(next_function)
        return self

    def __call__(self,*args):
        """
        calling the pipe will execute. You can pass more arguments here.
        """
        g = self.computation.pop(0)(*self.args , *args)
        for f in self.computation:
            g = f(g)
        return g

    def __lshift__(self, other):
        """
        pipe arguments in. They are appended after whatever you just passed.
        Multiple arguments can be passed as a tuple.

        """
        if isinstance(other, tuple):
            other = list(other)
            args = list(self.args)
            for k,i in enumerate(args):
                if isinstance(i, PlaceHolderArg):
                    arg = other.pop(0)
                    args[k] = arg
                else:
                    continue
            self.args = (*args,*other)
        else:
            for k,i in enumerate(self.args):
                if isinstance(i, PlaceHolderArg):
                    args = list(self.args)
                    args[k] = other
                    other = None
                    self.args = tuple(args)
                    break
            if other != None:
                self.args = (*self.args,other )

        self = self.__call__()
        return self


# pipe first argument in Pipe() call, second argument with left pipe
p = Pipe(2) >> (lambda x,y:2*x + y)  << 3.
print(p)

# pipe second argument in Pipe() using a placeholder for first arg, first argument with left pipe
_ = PlaceHolderArg()
p = Pipe(_,2) >> (lambda x,y:2*x + y)  << 3.
print(p)

# more complicated:
def f(a,b,c,d):
    return a,b,c,d
p = Pipe(_,2.,_,4.) >> f  << (1.,3.)
print(p)
