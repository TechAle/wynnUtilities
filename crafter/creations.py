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
    output = {}
    for ing in ings["ingredients"]:
        output[ing["name"]] = {
            "tier": ing["tier"],
            "level": ing["level"],
            "professions": ing["professions"],
            "statuses": ing["statuses"],
            "itemModifiers": ing["itemModifiers"],
            "ingredientModifiers": ing["ingredientModifiers"]
        }
    with open('./crafter/dataset/ings.json', 'w') as fp:
        json.dump(output, fp)
