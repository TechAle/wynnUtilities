
def askPlayerToStalk():
    while True:
        inp = input("Players (name, name): ")
        if len(inp := inp.strip().split(",")) > 0:
            return inp


def generalIntAsk(shown, maxNumber):
    while True:
        if (choose := input(shown)).isnumeric() \
                and (choose := int(choose)) > 0 and choose <= maxNumber:
            return choose


def askServer():
    while True:

        if (choose := input("Server (all-number-number,number):")).isnumeric() and (
                (choose := int(choose)) > 0 and choose <= 50) \
                or (type(choose) == str and choose.lower() == "all") or (
                choose.__contains__(",") and len(choose := choose.split(",")) > 0):
            return choose

def generalStringAsk(shown, answers, trueAnswer=None):
    while True:
        if answers.__contains__((choose := input(shown + "\nChoose: ")).lower()):
            return choose == trueAnswer if trueAnswer is not None else choose

