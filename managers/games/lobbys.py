import json
import random
import time
#Shows cliant errors
def error(error_code=""):
  return {"status":False, "error":error_code}
#Returns data
def ret_data(data=""):
  return {"status":True, "data":data}


def dead_lobby_scan():
  lobbys = json.loads(open("data/gamelobby.json","r").read())
  #initTime
  for x in lobbys:
    if time.time() - x["initTime"] > 1800:
      print("DEAD")


def search_users(searchType, searchTerm):
  #Searches through users
  # if searchType 1 = by token, 2 = by name 
  users = json.loads(open("data/userdata.json").read())
  out = []
  
  for x in users:
    if searchType == 1:
      if x["token"] == searchTerm:
        out.append(x)
    elif searchType == 2:
      if x["user"] == searchTerm:
        out.append(x)
  #Checks if there are none
  if len(out) == 0:
    out = None
  #sends all users back
  return out








def createLobby(data):

  #Check if user valid and who it is
  bruuu = search_users(1, data["token"])
  if len(bruuu) > 0:
    bruuu = bruuu[0]


    #Create and define lobby data
    tmp = {}
    tmp["lobbyName"] = data["lobbyName"]
    tmp["type"] = data["type"]
    tmp["users"] = [
      {
        "name":bruuu["user"],
        "token":bruuu["token"],
        "user_type":2
      }
    ]
    tmp["id"] = random.randint(10000000, 99999999)
    tmp["joinCode"] = random.randint(10000,99999)
    tmp["initTime"] = time.time()


    # Load in all the lobbys for modification
    f = json.loads(open("data/gamelobby.json", "r").read())
    #append the new lobby to the list
    f.append(tmp)

    #Save all of the lobbys including the new one
    with open("data/gamelobby.json", "w") as turd:
      turd.write(json.dumps(f, indent = 4))
      turd.close()

    return_data = {
      "lobbyName":tmp["lobbyName"],
      "lobbyId":tmp["id"],
      "joinCode":tmp["joinCode"],
      "users":[
        {
          "name":bruuu["user"],
          "user_type":2
        }
      ]
    }

    return ret_data(return_data)

  else:
    error("Bad Token")