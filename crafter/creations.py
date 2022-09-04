import json

from api import WynnPy


def createDatalist():
    wynnApi = WynnPy.wynnPy()
    ings = wynnApi.getIngridients()
    modifiers = []
    for ing in ings["ingredients"]:
        for modifier in ing["statuses"]:
            if not modifiers.__contains__(modifier):
                modifiers.append(modifier)
    header = '<datalist id="modifiers">'
    body = ''
    for modifier in modifiers:
        body += f'<option value="{modifier}"></option>'
    footer = '</datalist>'
    print(header + body + footer)


def powderToReq(powder):
    if powder == "Earth":
        return "strength"
    elif powder == "Water":
        return "intelligence"
    elif powder == "Thunder":
        return "dexterity"
    elif powder == "Fire":
        return "defense"
    elif powder == "Air":
        return "agility"


def createDataset():
    wynnApi = WynnPy.wynnPy()
    ings = wynnApi.getIngridients()
    ingsOutput = {}
    professions = {}
    itemModifiers = {}
    statuses = {}
    types = {}
    ingModifiers = {}
    # Add powders
    kinds = ["Earth", "Water", "Thunder", "Fire", "Air"]

    powders = {
        1: {
            "durability": -35,
            "neutral": -37,
            "damage": 40,
            "req": 0
        },
        2: {
            "durability": -52.5,
            "neutral": -46,
            "damage": 51,
            "req": 0
        },
        3: {
            "durability": -70,
            "req": 10,
            "neutral": -55,
            "damage": 62
        },
        4: {
            "durability": -91,
            "req": 20,
            "neutral": -68,
            "damage": 75
        },
        5: {
            "durability": -112,
            "req": 28,
            "neutral": -84,
            "damage": 92
        },
        6: {
            "durability": -133,
            "req": 36,
            "neutral": -102,
            "damage": 112
        }
    }
    for kind in kinds:
        for powder in powders:
            ings["ingredients"].append({
                "name": f"{kind} powder {powder}",
                "tier": 0,
                "level": 0,
                "professions": ["ARMOURING", "TAILORING",
                                "WEAPONSMITHING", "WOODWORKING",
                                "JEWELING"],
                "statuses": {},
                "ingredientModifiers": {},
                "itemModifiers": {
                    "durability": powders[powder]["durability"],
                    powderToReq(kind): powders[powder]["req"],
                    kind: powders[powder]["damage"],
                    "neutral": powders[powder]["neutral"]
                }
            })
    for ing in ings["ingredients"]:
        for prof in ing["professions"]:
            if not professions.__contains__(prof):
                professions[prof] = professions.__len__()
        for ingMod in ing["ingredientModifiers"]:
            if not ingModifiers.__contains__(ingMod):
                ingModifiers[ingMod] = ingModifiers.__len__()
        for mod in ing["itemModifiers"]:
            if not itemModifiers.__contains__(mod):
                itemModifiers[mod] = itemModifiers.__len__()
        for stat in ing["statuses"]:
            if not statuses.__contains__(stat):
                statuses[stat] = statuses.__len__()
            if not types.__contains__(ing["statuses"][stat]["type"]):
                types[ing["statuses"][stat]["type"]] = types.__len__()

        profToAdd = []
        for prof in ing["professions"]:
            profToAdd.append(professions[prof])

        ingModifs = {}
        for ingMod in ing["ingredientModifiers"]:
            ingModifs[ingModifiers[ingMod]] = ing["ingredientModifiers"][ingMod]

        statusesToAdd = {}
        for status in ing["statuses"]:
            statusesToAdd[statuses[status]] = {
                "type": types[ing["statuses"][status]["type"]],
                "min": ing["statuses"][status]["minimum"],
                "max": ing["statuses"][status]["maximum"]
            }

        itemModToAdd = {}
        for mod in ing["itemModifiers"]:
            itemModToAdd[itemModifiers[mod]] = ing["itemModifiers"][mod]

        ingsOutput[ing["name"]] = {
            "tier": ing["tier"],
            "level": ing["level"],
            "professions": profToAdd,
            "statuses": statusesToAdd,
            "itemModifiers": itemModToAdd,
            "ingredientModifiers": ingModifs
        }

    with open('./crafter/dataset/ings.json', 'w') as fp:
        json.dump(ingsOutput, fp, indent=4)

    professions = {v: k for k, v in professions.items()}
    with open('./crafter/dataset/prof.json', 'w') as fp:
        json.dump(professions, fp, indent=4)
    itemModifiers = {v: k for k, v in itemModifiers.items()}
    with open('./crafter/dataset/itemMods.json', 'w') as fp:
        json.dump(itemModifiers, fp, indent=4)
    statuses = {v: k for k, v in statuses.items()}
    with open('./crafter/dataset/stats.json', 'w') as fp:
        json.dump(statuses, fp, indent=4)
    ingModifiers = {v: k for k, v in ingModifiers.items()}
    with open('./crafter/dataset/ingModifiers.json', 'w') as fp:
        json.dump(ingModifiers, fp, indent=4)


if __name__ == "__main__":
    print("Please run setup.py not this")
    exit(-1)
