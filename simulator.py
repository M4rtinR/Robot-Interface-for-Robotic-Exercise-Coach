FILENAME = "P4.1.log"
AMorPM = " AM "


def get_data_from_file(filename):
    f = open("/home/martin/PycharmProjects/RobotTest/Study1LogFiles/" + filename, "r")
    lines = f.readlines()
    f.close()

    data = []

    for line in lines:
        second_half = line.split(AMorPM)
        if second_half[:8] == "Received":
            data_item = second_half[24:]
            data.append(data_item)
            print(data_item)


if __name__ == "__main__":
    get_data_from_file(FILENAME)
