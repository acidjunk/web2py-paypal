#from paypalrestsdk.resource import Find, Create
from resource import Find, Create

# == Example
#   credit_card = CreditCard.find("CARD-5BT058015C739554AKE2GCEI")
#   credit_card = CreditCard.new({'type': 'visa'})
#
#   credit_card.create()  # return True or False
class CreditCard(Find, Create):

  path = "v1/vault/credit-card"

CreditCard.convert_resources['credit_card'] = CreditCard
