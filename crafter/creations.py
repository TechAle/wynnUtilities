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


def createDataset():
    wynnApi = WynnPy.wynnPy()
    ings = wynnApi.getIngridients()
    ingsOutput = {}
    professions = {}
    itemModifiers = {}
    statuses = {}
    types = {}
    ingModifiers = {}
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
