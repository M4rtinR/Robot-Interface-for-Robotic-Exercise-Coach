if __name__ == "__main__":
    f = open("/home/martin/PycharmProjects/RobotTest/SessionDataFiles/P2", "w")
    f.write("Test 1\nTest 2\nTest 3")
    f.close()
    participantNo = "P2.1"
    performance = 2
    filename = participantNo.split(".")[0]
    f = open("/home/martin/PycharmProjects/RobotTest/SessionDataFiles/" + filename, "r")
    lines = f.readlines()
    print(lines)
    f.close()
    lines[1] = "Test 4\n"
    f = open("/home/martin/PycharmProjects/RobotTest/SessionDataFiles/" + filename, "w")
    session_no = participantNo.split(".")[1]
    f.writelines(lines)
    f.close()

    f = open("/home/martin/PycharmProjects/RobotTest/SessionDataFiles/" + filename, "r")
    print(f.read())
    f.close()
