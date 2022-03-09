import json
import utils
from managers.users import auth




def getitems(token):

  shopData = json.loads(open("settings/shop.json", "r").read())
  cards = json.loads(open("settings/cards.json", "r").read())
  abilitys = json.loads(open("settings/abilitys.json", "r").read())

  # search for user
  user = auth.search_users(1, token)

  # see if search came up with anything
  if (user):
    user = user[0]
    tmp = []

    # go through the shop
    for x in shopData:

      
      tmp2 = utils.search_for_card(x["itemID"])

      if tmp2:
        tmp3 = x
        tmp3["cardData"] = tmp2 

        if tmp2["ability"]:
          tmp3["abilityDisc"] = abilitys[tmp2["ability"]-1]

        tmp.append(tmp3)



    return utils.ret_data({"cards":tmp, "userMoney":user["data"]["money"]})

  else:
    return utils.error("Bad token")

def buyitem(data):

  # Search for user
  user = auth.search_users(1, data["token"])
  shopData = json.loads(open("settings/shop.json", "r").read())
  cards = json.loads(open("settings/cards.json", "r").read())

  # See if search returned anything
  if (user):
    user = user[0]
    shopItem = None
    # make sure item exists and fetch item data
    for item in shopData:
      if data["item"] == item["id"]:
        shopItem = item
        break
    if shopItem:


      if user["data"]["money"] >= shopItem["price"]:
        
        itemID = shopItem["itemID"]
        
        user["data"]["money"] = user["data"]["money"] - shopItem["price"]

        user["data"]["cards"].append(itemID)

        utils.update_userdata(data["token"], user)
        
        return utils.ret_data("Card bought successfully.")
      else:
        return utils.error("Not enough money!")
    
      pass

    else:
      return utils.error("Bad shop Id")

    pass



  else:
    return utils.error("Bad Token")