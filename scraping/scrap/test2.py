from pprint import pp
import json
kym = json.load(open("kym.json", 'r', encoding='utf8'))
for entry in kym:
    if entry['title'].lower() == 'one does not simply walk into mordor':
        pp(entry)
        break
