import api.WynnPy

def main():
    a = api.WynnPy.wynnPy()
    output = a.getPlayerStats("NoCatsNoLife")
    print(output)


if __name__ == "__main__":
    main()