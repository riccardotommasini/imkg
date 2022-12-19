import json
data = {}
import re

with open('kym_vision3.json', encoding='utf8') as f:
    data = json.load(f)
    print(len(data))
with open('kym_vision5.json', encoding='utf8') as f:
    data2 = json.load(f)
    print(len(data2))
    data.update(data2)
print(len(data))
with open('kym_vision_done.json', 'w', encoding='utf8') as f:
    json.dump(data, f, ensure_ascii=False)
