import api.WynnPy

def main():
    wynnApi = api.WynnPy.wynnPy()
    ## Get players
    players = wynnApi.getWynnClass("NoCatsNoLife", "shaman")


if __name__ == "__main__":
    main()