import numpy
import random

class CA(object):
    def __init__(self, rule, n=100, ratio=2):
        self.table = make_table(rule)
        self.n = n
        self.m = ratio*n + 1
        self.array = numpy.zeros((n, self.m), dtype=numpy.int8)
        self.next = 0

    def start_single(self):
        '''Starts with one cell in the middle of the top row'''
        self.array[0, self.m/2] = 1
        self.next += 1

    def start_random(self):
        '''Starts with a random configuration of cells in the top row'''
        for i in xrange(self.m):
            if random.random() >= .5: self.array[0, i]  = 1

        self.next += 1

    def start_comp(self):

        # pattern = [1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0]
        pattern = [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1]
        for i in xrange(self.m):
            j = i%len(pattern)
            self.array[0, i] = pattern[j]

        # self.array[0, self.m/2] = 1
        # self.array[0, (self.m/2) + 1] = 0
        # self.array[0, (self.m/2) + 2] = 0
        # self.array[0, (self.m/2) + 3] = 0
        # self.array[0, (self.m/2) + 4] = 1
        self.next += 1

    def step(self):
        '''Compute the next row of the CA'''
        i = self.next
        self.next += 1

        a = self.array
        t = self.table
        for j in xrange(1, self.m-1):
            a[i,j] = t[tuple(a[i-1, j-1:j+2])]

    def loop(self, n):
        [self.step() for i in xrange(n)]

    def get_array(self, start=0, end=None):
        if start==0 and end==None:
            return self.array
        else:
            return self.array[:, start:end]

def make_table(rule):
    bits = [tuple(int(char) for char in binary(7-i, 3)) for i in xrange(8)]
    bins = [char for char in binary(rule, 8)]

    return dict(zip(bits, bins))

def binary(n, l):
    b = bin(n)[2:]
    len_b = len(b)
    if len_b <= l:
        return '0'*(l-len_b) + b

print binary(8, 8)
print make_table(50)
