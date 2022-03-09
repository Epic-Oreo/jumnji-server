import json
import utils
import random
from managers.users import auth

def getItems(data):
  user = auth.search_users(1, data["token"])

  tradingHall = json.loads(open("data/tradingHall.json", "r").read())

  abilitys = json.loads(open("settings/abilitys.json", "r").read())

  if user:
    user = user[0]
    outData = []
    
    for item in tradingHall:
      if item["creator"]["token"] != user["token"]:

        cardInfo = utils.search_for_card(item["cardID"])

        if cardInfo:
          tmp = "None"
          for ability in abilitys:
            if ability["id"] == cardInfo["ability"]:
              if ability["discription"]:
                tmp = "{} ({})".format(ability["name"], ability["discription"])
              else:
                tmp = ability["name"]

        else:
          tmp = "None"
          cardInfo = "NO CARD!"
        


        outData.append(
          {
            "creator":{
              "name":item["creator"]["name"],
            },
            "id": item["id"],
            "cardID":item["cardID"],
            "cardInfo":cardInfo,
            "price":item["price"],
            "abilityDisc":tmp
          }
        )

    return utils.ret_data({"cards":outData, "money":user["data"]["money"]})
  else:
    return utils.error("Bad Token!")



def postItem(data):

  # {"cardID":8857721281,
  # "price":10,
  # "process":"postItem"
  # ,"token":"6c63d35d-42f4-436a-95ae-586c830a44f2"}

  user = auth.search_users(1, data["token"])

  if user:
    user = user[0]

    if data["cardID"] in user["data"]["cards"]:
      user["data"]["cards"].remove(data["cardID"])
      utils.update_userdata(data["token"], user)

      hallItems = json.loads(open("data/tradingHall.json").read())

      hallItem =   {
        "creator":{
          "name":user["user"],
          "token":user["token"]
        },
        "id": random.randint(100000000,9999999999),
        "cardID":data["cardID"],
        "price":data["price"]
      }

      hallItems.append(hallItem)

      with open("data/tradingHall.json", "w") as f:
        f.write(json.dumps(hallItems, indent=4))
        f.close()

      

      return utils.ret_data("Card Added")

    else:
      return utils.error("Card Id error")
    
    
  else:
    return utils.error("Bad Token")

  return utils.ret_data(data)




def buyItem(data):

  user = auth.search_users(1, data["token"])

  tradeHallItems = json.loads(open("data/tradingHall.json", "r").read())

  cards = json.loads(open("settings/cards.json", "r").read())

  if user:
    user = user[0]
    selectedItem = None
    for item in tradeHallItems:
      if str(item["id"]) == str(data["item"]):
        selectedItem = item
    if selectedItem:
      if user["data"]["money"] >= selectedItem["price"]:
        user["data"]["money"] -= selectedItem["price"]
        user["data"]["cards"].append(selectedItem["cardID"])
        utils.update_userdata(data["token"], user)



        sellerUser = selectedItem["creator"]["token"]
        sellerUser = auth.search_users(1, sellerUser)[0]

        sellerUser["data"]["money"] += selectedItem["price"]

        utils.update_userdata(sellerUser["token"], sellerUser)



        tradeHallItems = json.loads(open("data/tradingHall.json", "r").read())
        for item2 in tradeHallItems:
          if str(item2["id"]) == str(data["item"]):
            tradeHallItems.remove(item2)

        with open("data/tradingHall.json", "w") as f:
          f.write(json.dumps(tradeHallItems, indent=4))
          f.close()

        return utils.ret_data("Purchase Successful")
      else:
        return utils.error("Not enough money")
    else:
      return utils.error("Bad Item")
  else:
    return utils.error("Bad Token")