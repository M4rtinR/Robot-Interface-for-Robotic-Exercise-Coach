import ast

if __name__ == "__main__":
    '''string = "15 mtrs\/sec"
    scoreString = string[:-10]
    print(scoreString)

    scoreStringInt = int(scoreString)
    print(scoreStringInt)

    scoreStringIntSum = scoreStringInt + 1
    print(scoreStringIntSum)'''

    cumulative_reward = 60.4
    policy_matrix = [[0.4, 0.2, 0.2, 0.1, 0.2], [0.4, 0.0, 0.0, 0.1, 0.5]]

    try:
        f = open("/home/martin/PycharmProjects/RobotTest/SessionDataFiles/P3", "r")
        file_contents = f.readlines()
        f.close()

        f = open("/home/martin/PycharmProjects/RobotTest/SessionDataFiles/P3", "w")
        file_contents.insert(0, str(cumulative_reward) + "\n")
        file_contents.insert(0, str(policy_matrix) + "\n")
        print(file_contents)
        f.writelines(file_contents)
        f.close()
    except:
        f = open("/home/martin/PycharmProjects/RobotTest/SessionDataFiles/P3", "a")
        file_contents = [str(policy_matrix) + "\n", str(cumulative_reward) + "\n"]
        f.writelines(file_contents)
        f.close()

    '''aggregator_contents = [0]

    write_lines.insert(0, str(2.54) + "\n")
    write_lines.insert(1, str(5) + "\n")

    this_session_line_no = 2
    while len(write_lines) > this_session_line_no:
        stat = write_lines[this_session_line_no]
        this_session_line_no += 1
        if not (stat in aggregator_contents):
            aggregator_contents.append(stat)
            aggregator_contents.append(write_lines[this_session_line_no])
        else:
            index = aggregator_contents.index(stat)
            aggregator_contents[index + 1] = write_lines[this_session_line_no]

        # Update baseline file
        # index = baseline_contents.index(stat)
        # baseline_contents[index + 1] = this_session_contents[this_session_line_no]

        this_session_line_no += 1
        lines_to_add = int(write_lines[this_session_line_no]) + 1
        this_session_line_no += lines_to_add

    print(write_lines)
    print(aggregator_contents)'''


    '''f = open("/home/martin/PycharmProjects/RobotTest/SessionDataFiles/P2", "w")
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
    f.close()'''
