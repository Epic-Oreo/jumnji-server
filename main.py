from flask import Flask, render_template, request, send_from_directory
import os, json

from managers.users import auth

from managers.users import guilds

from managers.users import utilitys

from managers.games import lobbys

from managers.shop import shop

from managers.shop import playerShop

from managers.shop import pack as packShop


import utils

def search(searchType, searchTerm):
  #Searches through users
  # if searchType 1 = by token, 2 = by name 
  return utils.search_users(searchType, searchTerm)

def check_if_admin(token):
  return utils.check_if_admin(token)


#Shows cliant errors
def error(error_code):
  return {"status":False, "error":error_code}
#Returns data
def ret_data(data):
  return {"status":True, "data":data}

app = Flask(
  __name__,
  template_folder='webdata/templates',
  static_url_path="/webdata/static", 
  static_folder='webdata/static'
)
from webdata import web


@app.route('/')
@app.route("/index")
def index():
  return render_template("index.html")

#Assigns data
@app.route('/server/usermanage', methods=["post"])
def server_usermanage():
  data = request.json
  if data["process"] == "login":
    return auth.login(data)
  
  elif data["process"] == "signup":
    return auth.signup(data) # yo?

  elif data["process"] == "guilds":
    return guilds.createguild(data)

  elif data["process"] == "getCards":
    return utilitys.getCards(data["token"])

  elif data["process"] == "update":
    return utilitys.update(data["token"])

  else:
    return {"status":False,"error":"That Process did not exist"}



@app.route("/server/ping", methods=["post"])
def ping():
  return "Pong"


@app.route('/server/gamemanage', methods=["post"])
def server_gamemanage():
  data = request.json

  print(data)
  
  if data["process"] == "createLobby":
    return lobbys.createLobby(data)

  else:
    return error("Not a preocess")

@app.route("/server/shopmanage", methods=["post"])
def server_shopmanage():
  data = request.json

  # Card Shop

  if data["process"] == "getShopItems":
    return shop.getitems(data["token"])

  elif data["process"] == "buyItem":
    return shop.buyitem(data)


  # Trading Hall

  elif data["process"] == "getPlayerShop":
    return playerShop.getItems(data)

  elif data["process"] == "postItem":
    return playerShop.postItem(data)
  
  elif data["process"] == "buyPlayerItem":
    return playerShop.buyItem(data)


  # Pack Shop


  elif data["process"] == "getPacks":
    return packShop.getPacks(data)
  elif data["process"] == "buyPack":
    return packShop.buyPack(data)

app.run(host='0.0.0.0', port=8080)

