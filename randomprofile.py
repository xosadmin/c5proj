import pycountry,random

countries = list(pycountry.countries)
nouns = ['tiger', 'dragon', 'eagle', 'phoenix', 'wolf', 'lion', 'panther', 'hawk', 'bear', 'shark', 'snake', 'fox',
         'sparrow', 'owl', 'raven', 'gazelle', 'whale', 'dolphin', 'leopard', 'unicorn']
adjectives = ['fierce', 'mighty', 'swift', 'majestic', 'powerful', 'savage', 'brave', 'wild', 'elegant',
              'mysterious', 'ferocious', 'legendary', 'cunning', 'fearless', 'noble', 'sly', 'graceful',
              'furious', 'bold', 'mystical']


def randomCountry():
    tempcountry = random.sample(countries, 1)
    for country in tempcountry:
        return country.name

def randomNickname():
    composeName = nouns[random.randint(0,len(nouns)-1)] + "_" + adjectives[random.randint(0,len(adjectives)-1)]
    return composeName
