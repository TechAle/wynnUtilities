from api import WynnPy


def createDatalist():
    wynnApi = WynnPy.wynnPy()
    ings = wynnApi.getIngridients()
    modifiers = []
    for ing in ings["ingredients"]:
        for modifier in ing["statuses"]:
            if not modifiers.__contains__(modifier):
                modifiers.append(modifier)
    b = 0
    header = '<datalist id="modifiers">'
    body = ''
    for modifier in modifiers:
        body += f'<option value="{modifier}"></option>'
    footer = '</datalist>'
    print(header + body + footer)


createDatalist()