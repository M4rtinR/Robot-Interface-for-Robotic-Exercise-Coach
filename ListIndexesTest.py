import random

def countCats(category, thisList):
    count = 0
    for element in thisList:
        if category == 0:
            if element < 5:
                count += 1
        elif category == 1:
            if element < 10 and element > 4:
                count += 1
        else:
            if element > 9:
                count += 1

    return count

if __name__ == "__main__":
    '''testList = ["racketPreparation", "97.0, 0.0, 4, ", "approachTiming", "22.0, 0.29128176, ", "impactCutAngle", "11.0, 0.0, 4, ", "racketPreparation", "95.0, 0.033452, "]

    indices = [i for i, e in enumerate(testList) if e == "racketPreparation"]
    index = indices[len(indices) - 1] + 1
    print("index = " + str(index) + ", value = " + testList[index])'''

    used_behaviours = []
    for i in range(10):
        print("Used behaviours = " + str(used_behaviours))
        behaviour = random.randint(0, 15)
        print("bheaviour = " + str(behaviour))
        if behaviour == 0 or behaviour == 1 or behaviour == 2 or behaviour == 3 or behaviour == 4:
            category = 0
        elif behaviour == 5 or behaviour == 6 or behaviour == 7 or behaviour == 8 or behaviour == 9:
            category = 1
        else:
            category = 2
        print("category = " + str(category))
        cat0count = countCats(0, used_behaviours)
        cat1count = countCats(1, used_behaviours)
        cat2count = countCats(2, used_behaviours)
        print("category0 count = " + str(cat0count) + "category1 count = " + str(cat1count) + "category2 count = " + str(cat2count))

        if category == 0 and cat0count > 1:
            behaviour = 1
        elif category == 1 and cat1count > 1:
            behaviour = 1
        elif category == 2 and cat2count > 1:
            behaviour = 1

        print("behaviour = " + str(behaviour))
        used_behaviours.append(behaviour)

