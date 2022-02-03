import json

from django.test import TestCase


# Create your tests here.
class A:
    def __init__(self, a, b, c, name):
        self.a = a
        self.b = b
        self.c = c
        self.name = name
    # def __str__(self):
    #     return self.name


class B:
    def __init__(self):
        self.c = 7

    # def __str__(self):
    #     return 'd'


a = A(1, 2, 3,'a')
b = A(4, 5, 6,'b')
c = A(7, 8, 9,'c')
d = B()
l = [a, b, c, d]
l=sorted(l,key=lambda x: x.c)
for i in l:
    print(i)
# print(l)
a=[3,4,5,6]
# print(list(map(lambda x: x + 2, a)))
# a=a.pop(5)
a.remove(5)
print(a)
# print(a.pop(5))

a=1 and 0 or 1 and 0
print(a)
a=[{'a':3},{'a':4}]
print(json.dumps(a))