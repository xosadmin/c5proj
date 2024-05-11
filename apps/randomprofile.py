import pycountry,random
import secrets
import uuid

countries = list(pycountry.countries)
nouns = ['tiger', 'dragon', 'eagle', 'phoenix', 'wolf', 'lion', 'panther', 'hawk', 'bear', 'shark', 'snake', 'fox',
         'sparrow', 'owl', 'raven', 'gazelle', 'whale', 'dolphin', 'leopard', 'unicorn']
adjectives = ['fierce', 'mighty', 'swift', 'majestic', 'powerful', 'savage', 'brave', 'wild', 'elegant',
              'mysterious', 'ferocious', 'legendary', 'cunning', 'fearless', 'noble', 'sly', 'graceful',
              'furious', 'bold', 'mystical']
passwordDict = "1234567890abcdefghijklmnopqrstuvwxyz!@#$%^&*()_+[];',.-~<>?ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def randomCountry():
    tempcountry = random.sample(countries, 1)
    for country in tempcountry:
        return country.name

def randomEmail():
    composeEmailAddr = nouns[random.randint(0,len(nouns)-1)] + str(random.randint(0,1000)) + "@test.com"
    return composeEmailAddr

def generatePassword(length):
    lenpwddict = len(passwordDict)
    composePassword = ""
    for i in range(0,length):
        composePassword += passwordDict[random.randint(0,lenpwddict-1)]
    return composePassword

def randomSessionKey(length):
    return secrets.token_hex(length)

def randomPinCode():
    return random.randint(1000,9999)

def randomCoinRewards():
    number = int(random.randint(0,10))
    return number

def uuidGen():
    uuidGened = str(uuid.uuid4())
    return uuidGened
