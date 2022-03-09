import json
def makeguild(data):
  f = json.loads(open("guild.json", "r").read())
  f.append(data)
  with open("data/guild.json", "w") as turd:
    turd.write(json.dumps(f, indent = 4))
    turd.close()
  return "yay"