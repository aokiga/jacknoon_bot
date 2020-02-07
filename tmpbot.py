from collections import defaultdict

a = dict()
a[31] = 24
a[1] = 24
a[2] = 24
b = defaultdict()
b.update([(1,[2]), (2,[3]), (3, [4])])
b[1].append(12)
print(b[1])
