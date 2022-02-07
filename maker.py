if __name__ == "__main__":
  import json
  '''
  Rarity:
  1 = common
  2 = rare 
  3 = Epic
  4 = Mythic

  Elements:
  1 = fire
  2 = Water
  3 = air
  4 = Earth


  '''

  name = input("Name: ")
  rarity = int(input("rarity (1-4): "))
  element = int(input("element (1-4): "))
  tmp = input("ability: ")
  if tmp:
    ability = tmp
  else:
    ability = None
  health = int(input("health: "))
  damage = int(input("damage: "))
  f = json.loads(open("settings/cards.json", "r").read())
  f.append({
    "name":name,
    "rarity":rarity,
    "element":element,
    "ability":ability,
    "health":health,
    "damage":damage
  })

  with open("settings/cards.json", "w") as turd:
    turd.write(json.dumps(f, indent = 4))
    turd.close()