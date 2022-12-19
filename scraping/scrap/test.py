import json
from collections import Counter
kym = json.load(open("kym.json", 'r', encoding='utf8'))

stats = Counter()

sections = Counter()

for entry in kym:
    stats['entries'] += 1
    for k, v in entry.items():
        if v:
            stats[k] += 1
    if 'content' in entry:
        for k, v in entry['content'].items():
            if v:
                sections[k] += 1

    for k, v in entry['details'].items():
        if v:
            stats[k] += 1

for k, v in stats.most_common():
    if v < 287982:
        print(f"{k}: {v}")



print()
for k, v in sections.most_common(22):
    if v == 1: break
    print(f"{k}: {v}")
