import multiprocessing
import time
class Variables:
    def __init__(self, namespace, lock):
        self.ns = namespace
        self.lock = lock
        self.ns.a = []
        self.ns.b = []
        self.ns.c = 0

    @property
    def a(self):
        return self.ns.a

    @a.setter
    def a(self, value):
        self.ns.a = value

    @property
    def b(self):
        return self.ns.b

    @b.setter
    def b(self, value):
        self.ns.b = value

    @property
    def c(self):
        return self.ns.c

    @c.setter
    def c(self, value):
        self.ns.c = value
    def extend_to_variable(self, variable_name, value):

            current_variable = getattr(self.ns, variable_name)
            current_variable.extend(value)
            with self.lock:
                setattr(self.ns, variable_name, current_variable)

class methods:

    def __init__(self, variables):
        self.variables = variables

    def add(self,):
        # aa = []
        for i in range(10):
            # aa.extend([i])
            self.variables.extend_to_variable('a', [i])
        # variables.a = aa
    def print_var(self,):
        for i in range(10000):
            self.a = self.variables.a
            self.a = 10

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    lock = manager.Lock()
    ns = manager.Namespace()
    variables = Variables(ns, lock)

    print("Initial value of a:", variables.a)
    print("Initial value of b:", variables.b)

    start_time = time.time()
    mm = methods(variables)
    p1 = multiprocessing.Process(target=mm.add)
    p2 = multiprocessing.Process(target=mm.print_var)


    p1.start()

    p1.join()
    p2.start()
    p2.join()

    print("Final value of a:", variables.a)
    print("Final value of b:", variables.b)
    print("Time taken using pre-allocated NumPy array: {:.6f} seconds".format(time.time() - start_time))

