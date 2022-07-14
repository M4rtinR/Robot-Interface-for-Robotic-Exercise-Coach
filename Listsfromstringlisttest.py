list1 = "[0.1, 0.2, 0.3]"
list2 = "[1, 2, 3]"
list3 = "[3.123, 3.456, 3.789]"

stringList1 = list1.split(", ")
stringList2 = list2.split(", ")
stringList3 = list3.split(", ")

print("stringList1 = " + str(stringList1))
print("stringList2 = " + str(stringList2))
print("stringList3 = " + str(stringList3))

for i in range(len(stringList1)):
    if i == 0:
        floatList1 = [float(stringList1[i][1:])]
        floatList2 = [float(stringList2[i][1:])]
        floatList3 = [float(stringList3[i][1:])]
    elif i == len(stringList1) - 1:
        floatList1.append(float(stringList1[i][0:len(stringList1[i]) - 1]))
        floatList2.append(float(stringList2[i][0:len(stringList2[i]) - 1]))
        floatList3.append(float(stringList3[i][0:len(stringList3[i]) - 1]))
    else:
        floatList1.append(float(stringList1[i]))
        floatList2.append(float(stringList2[i]))
        floatList3.append(float(stringList3[i]))

print("floatList1 = " + str(floatList1))
print("floatList2 = " + str(floatList2))
print("floatList3 = " + str(floatList3))

aggregatedList = []
for list in [floatList1, floatList2, floatList3]:
    aggregatedList.append(sum(list) / len(list))

print("aggregatedList = " + str(aggregatedList))
