import json
import utils
from managers.users import auth


def getCards(token):

  user = auth.search_users(1, token)

  

  if user:
    user = user[0]
    out = []

    for card in user["data"]["cards"]:
      cardData = utils.search_for_card(card)
      out.append(cardData)

    return utils.ret_data(out)

  else:
    return utils.error("Bad Token")


def update(token):
  
  user = auth.search_users(1, token)
  if user:
    return user[0]
  else:
    return False