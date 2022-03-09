if __name__ == '__main__':
  import json
  import random
  import os
  def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
  '''

Earthquaker

Bone Chief  

  Rarity:
  1 = common
  2 = rare 
  3 = Epic
  4 = Mythic

  Elements:
  1 = Fire
  2 = Water
  3 = Air
  4 = Earth
  5 = Light
  6 = Darkness
  7 = Dream
  8 = Life

  Abilities:
"Freeze ray (opponent card is out for 2 rounds)",
    "id": 1
 "Cloraform (knocks out opponent card for a round",
    "id": 2
: "Fire breathing",
    "id": 3
 "Lightning powers",
    "id": 4
 "Tsunami!",
    "id": 5
 "Evil cactus attack",
    "id": 6
 "Shrink ray (lowers opponent's attack rate)",
    "id": 7
  '''
  abilitys = json.loads(open("settings/abilitys.json", "r").read())
  cls()
  name = input("Name: ")
  print("""1) common
2) rare 
3) Epic
4) Mythic""")
  rarity = int(input("rarity: "))
  cls()
  print("""1) Fire
2) Water
3) Air
4) Earth
5) Light
6) Darkness
7) Dream
8) Life""")
  element = int(input("element: "))
  cls()
  for ab in abilitys:
    print(str(ab["id"])+") "+str(ab["name"]))
  tmp = (input("ability (1 - 8): "))
  if tmp:
    ability = int(tmp)
  else:
    ability = None
  cls()
  health = int(input("health: "))
  damage = int(input("damage: "))
  cls()
  f = json.loads(open("settings/cards.json", "r").read())
  check = f
  x = True
  while x == True:
    for x in check:
      id = random.randint(10000000, 9999999999)
      if id == x["id"]:
        pass
      else:
        x = False
  f.append({
    "name":name,
    "rarity":rarity,
    "element":element,
    "ability":ability,
    "health":health,
    "damage":damage,
    "id":id,
    "visible":True
  })

  with open("settings/cards.json", "w") as turd:
    turd.write(json.dumps(f, indent = 4))
    turd.close()