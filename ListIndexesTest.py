if __name__ == "__main__":
    testList = ["racketPreparation", "97.0, 0.0, 4, ", "approachTiming", "22.0, 0.29128176, ", "impactCutAngle", "11.0, 0.0, 4, ", "racketPreparation", "95.0, 0.033452, "]

    indices = [i for i, e in enumerate(testList) if e == "racketPreparation"]
    index = indices[len(indices) - 1] + 1
    print("index = " + str(index) + ", value = " + testList[index])