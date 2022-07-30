if __name__ == "__main__":
    f = open("/home/martin/PycharmProjects/RobotTest/SessionDataFiles/P3", "a")
    write_lines = ["impactCutAngle\n", "18.0, 4,\n", "2\n", "12.0, 4,\n", "18.0, 4,\n", "followThroughRoll\n", "0.0, 5,\n", "2\n", "0.0, 4,\n", "0.0, 4,\n"]
    f.writelines(write_lines)
    f.close()

    aggregator_contents = [0]

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
    print(aggregator_contents)
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
