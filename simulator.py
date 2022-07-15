import requests

FILENAME = "P4.1.log"
AMorPM = " PM "
post_address = 'http://192.168.1.174:5000/cue'
baselineDone = False


def get_data_from_file(filename):
    f = open("/home/martin/PycharmProjects/RobotTest/Study1LogFiles/" + filename, "r")
    lines = f.readlines()
    f.close()

    data = []
    finalList = []

    for line in lines:
        second_half = line.split(AMorPM)[1]
        stringList = []
        if second_half[:8] == "Received":
            data_item = second_half[24:]
            data.append(data_item)
            # print(data_item)

            stringList = data_item.split(", ")
            # print(stringList)

        if not stringList == []:
            for i in range(len(stringList)):
                if i == 0:
                    # print("1: " + stringList[i][1:].split(": ")[0][0])
                    # print("2: " + stringList[i][1:].split(": ")[0][1:len(stringList[i][1:].split(": ")[0]) - 1])
                    # print("3: " + stringList[i][1:].split(": ")[1][0])
                    # print("4: " + stringList[i][1:].split(": ")[1][1:len(stringList[i][1:].split(": ")[1]) - 1])
                    setFromStringList = {(stringList[i][1:].split(": ")[0] if not stringList[i][1:].split(": ")[0][0] == "'" else stringList[i][1:].split(": ")[0][1:len(stringList[i][1:].split(": ")[0]) - 1]): (stringList[i][1:].split(": ")[1] if not stringList[i][1:].split(": ")[1][0] == "'" else stringList[i][1:].split(": ")[1][1:len(stringList[i][1:].split(": ")[1]) - 1])}
                elif i == len(stringList) - 1:
                    first = stringList[i].split(": ")[0]
                    second = stringList[i].split(": ")[1]
                    first = first.replace("'", "")
                    second = second.replace("'", "")
                    second = second.replace("}", "")
                    second = second.replace("\n", "")
                    setFromStringList[first] = second
                    # setFromStringList[stringList[i][0:len(stringList[i]) - 1].split(": ")[0] if not stringList[i][0:len(stringList[i]) - 1].split(": ")[0]] = stringList[i][0:len(stringList[i]) - 1].split(": ")[1]
                else:
                    first = stringList[i].split(": ")[0]
                    second = stringList[i].split(": ")[1]
                    first = first.replace("'", "")
                    second = second.replace("'", "")
                    setFromStringList[first] = second
                    # setFromStringList[stringList[i].split(": ")[0]] = stringList[i].split(": ")[1]

            print(setFromStringList)
            print(type(setFromStringList))
            finalList.append(setFromStringList)
    print(type(finalList))
    print(type(finalList[0]))
    return finalList

def simulate(data):
    print(type(data[0]))

    goal_level = 0

    while True:
        output = [n for i, n in enumerate(data) if n['goal_level'] == str(goal_level)][0]
        print("Output = " + str(output))
        data.remove(output)

        r = requests.post(post_address, json=output)
        while not r.status_code == 200:
            pass

        content = r.content
        print("Content = " + str(content))
        goal_level = int(content['goal_level'])
        if goal_level == 2 and not baselineDone:
            goal_level = 4
            baselineSet = True
        else:
            if content['completed'] == 0:
                goal_level += 1
            else:
                if goal_level == 4 and baselineSet:
                    goal_level = 3
                    baselineSet = False
                    baselineDone = True
                else:
                    goal_level -= 1

        print("New goal level = " + str(goal_level))


if __name__ == "__main__":
    data_list = get_data_from_file(FILENAME)
    simulate(data_list)
