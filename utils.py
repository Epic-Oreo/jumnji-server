import json, os
import requests


def getJson(fileName):
  return json.loads(open(fileName).read())


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


def update_userdata(token, data):
  selector = 0
  outSel = None
  allUsers = json.loads(open("data/userdata.json", "r").read())

  for user in allUsers:
    if user["token"] == token:
      outSel = selector
    selector += 1
  
  if outSel:
    
    allUsers[outSel] = data
    with open("data/userdata.json", "w") as f:
      f.write(json.dumps(allUsers, indent=4))
      f.close()

    return True

  else:

    return False
  


  pass

def get_abilitys(id):
  abilitys = json.loads(open("settings/abilitys.json", "r").read())
  for x in abilitys:
    if x["id"] == id:
      return x

def search_for_card(cardId):
  
  cards = json.loads(open("settings/cards.json", "r").read())
  for card in cards:
    if card["id"] == cardId:
      card["abilitysInfo"] = get_abilitys(card["ability"])
      return card
  return False


def check_if_admin(token):
  roles = json.loads(open("settings/roles.json", "r").read())

  for x in roles:
    # print(x["token"], token)
    if str(x["token"]) == str(token):
      if "admin" in x["roles"]:
        # print("RET TREU")
        return True
  else:
    return False



def majorError(text):
  key = os.getenv("mailAPI")

  url = "https://rapidprod-sendgrid-v1.p.rapidapi.com/mail/send"

  payload = {
      "personalizations": [
          {
              "to": [
                  {
                      "email": "oredgaming@gmail.com"
                  }
              ],
              "subject": "An error has accured in your Jumnji Server!!!!"
          }
      ],
      "from": {
          "email": "Error@th3lonius.com"
      },
      "content": [
          {
              "type": "text/plain",
              "value": "Error: "+str(text)
          }
      ]
  }
  payload = json.dumps(payload)
  headers = {
      'content-type': "application/json",
      'x-rapidapi-host': "rapidprod-sendgrid-v1.p.rapidapi.com",
      'x-rapidapi-key': "77130dd636msh389e821db430709p1c4775jsn4f54efb1d2cd"
      }

  response = requests.request("POST", url, data=payload, headers=headers)

  if response.status_code == 202:
    return True
  else:
    return False


  pass





#Shows client errors
def error(error_code):
  return {"status":False, "error":error_code}
#Returns data
def ret_data(data):
  return {"status":True, "data":data}
