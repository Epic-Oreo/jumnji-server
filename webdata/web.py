from __main__ import app

from __main__ import search

from __main__ import check_if_admin

from managers.users import auth

from managers.shop import playerShop

from flask import Flask, render_template, request, send_from_directory, redirect

import json

import utils

import base64

@app.route('/test', methods=['GET'])
def test():
    return 'it works!'


@app.route("/main", methods=["post", "get"])
def main():
  if request.method == 'POST':
    data = request.form
    data = data.to_dict()
    auth = False
    if data["loginType"] == "userPw":
      user = (search(2, data["username"]))
    elif data["loginType"] == "token":
      user = (search(1, data["token"]))
      if user:
        auth = True
    if user:
      user = user[0]
      if data["loginType"] == "userPw":      
        if data["password"] == user["pw"]:
          auth = True
      if auth:
        print(user)
        data["money"] = str(user["data"]["money"]) 
        data["userdata"] = user
        siteInfo = {}
        totalCards = 0
        cards = json.loads(open("settings/cards.json", "r").read())
        for x in cards:
          if x["visible"]:
            totalCards += 1
        siteInfo["totalCards"] = totalCards
        userCards = (data["userdata"]["data"]["cards"])
        tmp = []
        for x in userCards:
          if x not in tmp:
            tmp.append(x)
        tmp = len(tmp)
        siteInfo["userCards"] = (tmp)
        cardPrecentage = tmp/totalCards 
        siteInfo["cardPrec"] = round(cardPrecentage*100)
        isadmin = check_if_admin(user["token"])
        return render_template("main.html", data=data, isadmin=isadmin, siteInfo = siteInfo)

      else:
        return render_template("error.html", error="Bad Username or Password")

    else:
      return render_template("error.html", error="Bad Username or Password")

  else:
    return redirect("/")

@app.route("/main/command", methods=["post"])
def main_command():
  if request.method == 'POST':
    data = request.form

    if check_if_admin(data["token"]):
      command = data["command"]

      command = command.split(":")

      try:

        if command[0] == "viewUserData":
          user = search(2, command[1])
          return str(user)

        elif command[0] == "addCard":
          card = command[1]
          user = search(2, command[2])

          if user:
            user = user[0]
            user["data"]["cards"].append(int(card))
            utils.update_userdata(data["token"], user)
            return render_template("info.html", info="card added sucsefuly")
          else:
            return render_template("error.html", error="No user")

        elif command[0] == "checkAdmin":
          user = search(2, command[1])
          if user:
            user = user[0]
            if utils.check_if_admin(user["token"]):
              return render_template("info.html", info="Yes")
            else:
              return render_template("info.html", info="No")


          
      except Exception as error:
        return render_template("error.html", error = error)


    return redirect("/")
  else:
    return redirect("/")


@app.route("/tradehall", methods=["post", "get"])
def tradeHall():
  if request.method == "POST":
    data = request.form
    
    tradeItems = utils.getJson("data/tradingHall.json")
    
    user = auth.search_users(1, data["token"])
    if user:
      user = user[0]

      tmp = []
      for item in tradeItems:
        if item["creator"]["token"] != user['token']:
          item["cardDetails"] = utils.search_for_card(item["cardID"])
          item["cardParse"] = {"rarity":rarityParse(item["cardDetails"]["rarity"]), "element":elementsParse(item["cardDetails"]["element"])}
          if item["creator"]["token"] != data["token"]:
            item['creator']["token"] = ""
            tmp.append(item)
      

      if len(tmp) > 0:
        return render_template("tradeHall/tradeHall.html", items=tradeItems, userData=user)
      else:
        return render_template("info.html", info="There are no trade hall items available to you" )
    else:
      return render_template("error.html", error="Invalid Token")
    
    # return render_template("tradeHall/tradeHall.html")
  else:
    return render_template("tradeHall/getred.html")


@app.route("/tradehall/buy", methods=["post"])
def tradeHallBuy():
  data = request.form
  indata = {
  "token":data["token"],
  "item":data["item"]
  }
  retdata = playerShop.buyItem(data)

  if retdata["status"]:
    return render_template("info.html", info=retdata["data"])
  else:
    return render_template("error.html", error=retdata["error"])

  # return str(data)

def rarityParse(inp):
  if 1 == inp:
    return "Common"
  if 2 == inp:
    return "Rare"
  if 3 == inp:
    return "Epic"
  if 4 == inp:
    return "Mythic"

def elementsParse(inp):
  if 1 == inp:
    return "Fire"
  if 2 == inp:
    return "Water"
  if 3 == inp:
    return "Air"
  if 4 == inp:
    return "Earth"
  if 5 == inp:
    return "Light"
  if 6 == inp:
    return "Darkness"
  if 7 == inp:
    return "Dream"
  if 8 == inp:
    return "Life"



@app.route("/allCards")
@app.route("/allCards/")
@app.route("/allCards/<intoken>")
def allCards(intoken=None):
  
  incards = json.loads(open("settings/cards.json", "r").read())
  
  abilitys = json.loads(open("settings/abilitys.json", "r").read())

  cards = []
  isadmin = False
  if intoken:
    # print(intoken)
    try:
      isadmin = utils.check_if_admin(base64.b64decode(intoken).decode("utf-8") )
    except Exception as error:
      print(error)

  for card in incards:
    if card["visible"] or isadmin:
      card["elementName"] = elementsParse(card["element"])
      card["rarityName"] = rarityParse(card["rarity"])
      abilityName = ""
      abilityDisc = ""
      if card["ability"]:
        for x in abilitys:
          if x["id"] == card["ability"]:
            abilityName = x["name"]
            abilityDisc = x["discription"]

      card["abilityName"] = abilityName
      card["abilityDisc"] = abilityDisc
      
      cards.append(card)

  return render_template("allCards.html", cards=cards, isadmin=isadmin)