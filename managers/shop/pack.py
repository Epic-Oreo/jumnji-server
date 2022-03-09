import json
import utils
import random
from managers.users import auth


def getPacks(data):


  packs = utils.getJson("settings/packs.json")
  tmp = []
  for pack in packs:
    if pack["enabled"]:
      for item in pack["items"]:
        if item["type"] == "card":
          card = utils.search_for_card(item["id"])
          item["cardDetails"] = card
      tmp.append(pack)


  return utils.ret_data(tmp)



def buyPack(data):
  packs = utils.getJson("settings/packs.json")
  user = auth.search_users(1, data["token"])

  if user:
    user = user[0]
    selectedPack = None
    for pack in packs:
      if pack["id"] == data["packId"]:
        selectedPack = pack

    if selectedPack:      
      if user["data"]["money"] >= selectedPack["price"]:
        user["data"]["money"] -= selectedPack["price"]
        weights = []
        for item in selectedPack["items"]:
          weights.append(item["weight"])
        draw = random.choices(selectedPack["items"], weights=weights, k=1)[0]
        if draw["type"] == 'card':
          draw["cardData"] = utils.search_for_card(draw["id"])
          user["data"]["cards"].append(int(draw["id"]))
        
        elif draw["type"] == "money":
          user["data"]["money"] += int(draw["ammount"])

        utils.update_userdata(user["token"], user)

        return utils.ret_data(draw)

      else:
        return utils.error("Not Enough Money")
    else:
      return utils.error("Bad Pack ID")
  else:
    return utils.error("Bad Token!")