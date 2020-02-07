from collections import OrderedDict

score = OrderedDict([(1, 2), (3, 4), (2, 1)])

results = ''

score = OrderedDict(reversed(sorted(score.items(), key=(lambda x: x[1]))))
print(score)
for player_id, score in score.items():
    results += str(score) + '\n'

print(results)
