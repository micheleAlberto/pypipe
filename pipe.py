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
        g = self.computation.pop()(*self.args , *args)
        for f in self.computation:
            g = f(g)
        return g

    def __lshift__(self, other):
        """
        pipe arguments in. They are appended after whatever you just passed
        """
        #self.args = self.args + (other,) if len(self.args) > 0 else (other,)
        self.args = (*self.args,other)
        return self.__call__()
