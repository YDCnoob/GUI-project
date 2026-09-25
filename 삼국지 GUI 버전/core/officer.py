officers = [
    {
        "name": "유선",
        "faction": "촉",
        "leadership": 25,
        "war": 20,
        "intelligence": 45,
        "politics": 55,
        "charisma": 60,
    },
    {
        "name": "제갈량",
        "faction": "촉",
        "leadership": 92,
        "war": 38,
        "intelligence": 100,
        "politics": 98,
        "charisma": 92,
    },
    {
        "name" : "장비",
        "faction" : "촉",
        "leadership" : 75,
        "war" : 94,
        "intelligence" : 83,
        "politics" : 65,
        "charisma" : 79
    },
    {
        "name" : "관우",
        "faction" : "촉",
        "leadership" : 85,
        "war" : 95,
        "intelligence" : 82,
        "politics" : 85,
        "charisma" : 90
    },
    {
        "name" : "조운",
        "faction" : "촉",
        "leadership" : 89,
        "war" : 93,
        "intelligence" : 87,
        "politics" : 92,
        "charisma" : 95
    },
    {
        "name": "조인",
        "faction": "위",
        "leadership": 90,
        "war": 88,
        "intelligence": 72,
        "politics": 60,
        "charisma": 75,
    },
    {
        "name": "유기",
        "faction": "유표",
        "leadership": 55,
        "war": 40,
        "intelligence": 68,
        "politics": 72,
        "charisma": 74,
    },
]


def find_officer(name):
    for officer in officers:
        if officer["name"] == name:
            return officer

    return None


def get_officers_by_faction(faction):
    return [
        officer
        for officer in officers
        if officer["faction"] == faction
    ]

def get_city_faction(city):
    governor_name = city["governor"]

    if governor_name is None:
        return None

    governor = find_officer(governor_name)

    if governor is None:
        return None

    return governor["faction"]

def get_faction(name):
    officer = find_officer(name)

    if officer is None:
        return None

    return officer["faction"]

def get_available_governors(cities, faction):

    used_governors = [
        city["governor"]
        for city in cities
        if city["governor"] is not None
    ]

    return [
        officer
        for officer in officers
        if officer["faction"] == faction
        and officer["name"] not in used_governors
    ]