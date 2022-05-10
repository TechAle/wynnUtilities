# TODO: Try to merge some of these

def askPlayerToStalk():
    while True:
        inp = input("Players (name, name): ")
        if len(inp := inp.strip().split(",")) > 0:
            return inp

def askHunterCalling():
    while True:
        if type(choose := input("Hunter's calling? (y-n):")) == str and (
                choose := choose.lower()) == "y" or choose == "n":
            return choose == "y"

def askApi():
    while True:
        if (choose := input("Api:\n1) v2\n2) v3\nChoose: ")).isnumeric() \
                and (choose := int(choose)) > 0 and choose <= 2:
            return choose


def askServer():
    while True:

        if (choose := input("Server (all-number-number,number):")).isnumeric() and ((choose := int(choose)) > 0 and choose <= 50) \
                or (type(choose) == str and choose.lower() == "all") or (choose.__contains__(",") and len(choose := choose.split(",")) > 0):
            return choose

def askSingleOrWorld():
    while True:
        if type(choose := input("Single or World? (s-w):")) == str and (
                choose := choose.lower()) == "s" or choose == "w":
            return choose

def askFocus():
    while True:
        if type(choose := input("Focus? (y-n):")) == str and (
                choose := choose.lower()) == "y" or choose == "n":
            return choose == "y"