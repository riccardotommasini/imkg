import json

imagedata = json.load(open("kym_vision_done.json", encoding='utf8'))
kym = json.load(open("kym.json", encoding='utf8'))

missing = set()

for entry in kym:
    if entry['url'] not in imagedata:
        missing.add(entry['template_image_url'])

print(missing)