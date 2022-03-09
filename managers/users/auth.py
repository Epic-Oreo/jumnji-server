import json
from uuid import uuid4
import utils
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


#Checks if password is valid
def password_check(passwd):
    val = True
    if len(passwd) < 6:
        val = False
    if len(passwd) > 20:
        val = False
    if val:
        return val

#Shows client errors
def error(error_code):
  return {"status":False, "error":error_code}
#Returns data
def ret_data(data):
  return {"status":True, "data":data}


def login(data):
  username = data['user']
  password = data["pw"]
  user = search_users(2,username)
  if user:
    if len(user) > 1:
      utils.majorError("More than one account with same username [Auth.py login()]")

      return error("Error 10102 has occurred, This is a serious error and you will not be able to access your account until it is resolved, lol")
    else:
      user = user[0]
      if user["pw"] == password:
        return ret_data({"token":user["token"]})
      else:
        return error("That username or password is incorrect")  
  else:
    return error("That username or password is incorrect")


def signup(data):
  #Data = username & Password (This is not a line of code..)
  username = data["user"]
  password = data["pw"]
  #Searches by username
  existingUser = search_users(2, username)
  if existingUser:
    return error("That username is already taken")
  else:
    if password_check(password) and len(username) >= 4:
      tmp = {
        "user":username,
        "pw":password,
        "token":str(uuid4()),
        "data":{
            "money": 100,
            "cards": []
        }
      }
      fastData = json.loads(open("data/userdata.json", "r").read())

      fastData.append(tmp)

      with open("data/userdata.json", "w") as f:
        f.write(json.dumps(fastData, indent=4))
        f.close()
      return ret_data("Please now login")

    else:
      return error("Kill urself")

