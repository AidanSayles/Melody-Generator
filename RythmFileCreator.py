from itertools import permutations
import multiprocessing
import os

def permutateValueList(ValueList):
    ValueList = list(set(permutations(ValueList)))
    return ValueList

def unpackageList(mylist):
    newlist = []
    for chunk in mylist:
        for single in chunk:
            newlist.append(list(single))
    return newlist

def removeDuplicates(chunk, choice):
    tupleList = []
    listList = []
    for single in chunk:
        tupleList.append(tuple(single))
    tupleList = list(set(tupleList))
    if choice == 1:
        for single in tupleList:
            listList.append(list(single))
        return listList
    else:
        return tupleList

def combineRestsAndCounts(args):
    count, rest = args
    rythm = []
    for index, beat in enumerate(rest):
        rythm.append(beat + str(count[index]))
    return rythm

def combineRests(rythm):
    for i in range(4):
        for index, beat in enumerate(rythm):
            if beat[0] == 'O':
                if (index + 1) != len(rythm):
                    if rythm[index + 1][0] == 'O':
                        restLength1 = float(beat[1:])
                        restLength2 = float(rythm[index + 1][1:])
                        totalRestLength = restLength1 + restLength2
                        totalRestLength = 'O' + str(totalRestLength)
                        rythm[index] = totalRestLength
                        del restLength1
                        del restLength2
                        del totalRestLength
                        del rythm[index + 1]
    return rythm

fullCountsList = [
        [4],
        [3.75, 0.25],
        [3.5, 0.5],
        [3.5, 0.25, 0.25],
        [3.25, 0.75],
        [3.25, 0.5, 0.25],
        [3.25, 0.25, 0.25, 0.25],
        [3, 1],
        [3, 0.75, 0.25],
        [3, 0.5, 0.5],
        [3, 0.5, 0.25, 0.25],
        [3, 0.25, 0.25, 0.25, 0.25],
        [2.75, 1.25],
        [2.75, 1, 0.25],
        [2.75, 0.75, 0.5],
        [2.75, 0.75, 0.25, 0.25],
        [2.75, 0.5, 0.5, 0.25],
        [2.75, 0.5, 0.25, 0.25, 0.25],
        [2.75, 0.25, 0.25, 0.25, 0.25, 0.25],
        [2.5, 1.5],
        [2.5, 1.25, 0.25],
        [2.5, 1, 0.5],
        [2.5, 1, 0.25, 0.25],
        [2.5, 0.75, 0.75],
        [2.5, 0.75, 0.5, 0.25],
        [2.5, 0.75, 0.25, 0.25, 0.25],
        [2.5, 0.5, 0.5, 0.5],
        [2.5, 0.5, 0.5, 0.25, 0.25],
        [2.5, 0.5, 0.25, 0.25, 0.25, 0.25],
        [2.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [2.25, 1.75],
        [2.25, 1.5, 0.25],
        [2.25, 1.25, 0.5],
        [2.25, 1.25, 0.25, 0.25],
        [2.25, 1, 0.75],
        [2.25, 1, 0.5, 0.25],
        [2.25, 1, 0.25, 0.25, 0.25],
        [2.25, 0.75, 0.75, 0.25],
        [2.25, 0.75, 0.5, 0.25, 0.25],
        [2.25, 0.75, 0.25, 0.25, 0.25, 0.25],
        [2.25, 0.5, 0.5, 0.5, 0.25],
        [2.25, 0.5, 0.5, 0.25, 0.25, 0.25],
        [2.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25],
        [2.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [2, 2],
        [2, 1.75, 0.25],
        [2, 1.5, 0.5],
        [2, 1.5, 0.25, 0.25],
        [2, 1.25, 0.75],
        [2, 1.25, 0.5, 0.25],
        [2, 1.25, 0.25, 0.25, 0.25],
        [2, 1, 1],
        [2, 1, 0.75, 0.25],
        [2, 1, 0.5, 0.5],
        [2, 1, 0.5, 0.25, 0.25],
        [2, 1, 0.25, 0.25, 0.25, 0.25],
        [2, 0.75, 0.75, 0.5],
        [2, 0.75, 0.75, 0.25, 0.25],
        [2, 0.75, 0.5, 0.5, 0.25],
        [2, 0.75, 0.5, 0.25, 0.25, 0.25],
        [2, 0.75, 0.25, 0.25, 0.25, 0.25, 0.25],
        [2, 0.5, 0.5, 0.5, 0.5],
        [2, 0.5, 0.5, 0.5, 0.25, 0.25],
        [2, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25],
        [2, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [2, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1.75, 1.75, 0.5],
        [1.75, 1.75, 0.25, 0.25],
        [1.75, 1.5, 0.5],
        [1.75, 1.5, 0.25, 0.25],
        [1.75, 1.25, 0.5, 0.5],
        [1.75, 1.25, 0.5, 0.25, 0.25],
        [1.75, 1.25, 0.25, 0.25, 0.25, 0.25],
        [1.75, 1, 1, 0.25],
        [1.75, 1, 0.75, 0.5],
        [1.75, 1, 0.75, 0.25, 0.25],
        [1.75, 1, 0.5, 0.5, 0.25],
        [1.75, 1, 0.5, 0.25, 0.25, 0.25],
        [1.75, 1, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1.75, 0.75, 0.75, 0.75],
        [1.75, 0.75, 0.75, 0.5, 0.25],
        [1.75, 0.75, 0.75, 0.25, 0.25, 0.25],
        [1.75, 0.75, 0.5, 0.5, 0.5],
        [1.75, 0.75, 0.5, 0.5, 0.25, 0.25],
        [1.75, 0.75, 0.5, 0.25, 0.25, 0.25, 0.25],
        [1.75, 0.75, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1.75, 0.5, 0.5, 0.5, 0.5, 0.25],
        [1.75, 0.5, 0.5, 0.5, 0.25, 0.25, 0.25],
        [1.75, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1.75, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1.75, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1.5, 1.5, 1],
        [1.5, 1.5, 0.75, 0.25],
        [1.5, 1.5, 0.5, 0.5],
        [1.5, 1.5, 0.5, 0.25, 0.25],
        [1.5, 1.5, 0.25, 0.25, 0.25, 0.25],
        [1.5, 1.25, 1.25],
        [1.5, 1.25, 1, 0.25],
        [1.5, 1.25, 0.75, 0.5],
        [1.5, 1.25, 0.75, 0.25, 0.25],
        [1.5, 1.25, 0.5, 0.5, 0.25],
        [1.5, 1.25, 0.5, 0.25, 0.25, 0.25],
        [1.5, 1.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1.5, 1, 1, 0.5],
        [1.5, 1, 1, 0.25, 0.25],
        [1.5, 1, 0.75, 0.75],
        [1.5, 1, 0.75, 0.5, 0.25],
        [1.5, 1, 0.75, 0.25, 0.25, 0.25],
        [1.5, 1, 0.5, 0.5, 0.5],
        [1.5, 1, 0.5, 0.5, 0.25, 0.25],
        [1.5, 1, 0.5, 0.25, 0.25, 0.25, 0.25],
        [1.5, 1, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1.5, 0.75, 0.75, 0.75, 0.25],
        [1.5, 0.75, 0.75, 0.5, 0.5],
        [1.5, 0.75, 0.75, 0.5, 0.25, 0.25],
        [1.5, 0.75, 0.75, 0.25, 0.25, 0.25, 0.25],
        [1.5, 0.75, 0.5, 0.5, 0.5, 0.25],
        [1.5, 0.75, 0.5, 0.5, 0.25, 0.25, 0.25],
        [1.5, 0.75, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1.5, 0.75, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        [1.5, 0.5, 0.5, 0.5, 0.5, 0.25, 0.25],
        [1.5, 0.5, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25],
        [1.5, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1.25, 1.25, 1.25, 0.25],
        [1.25, 1.25, 1, 0.5],
        [1.25, 1.25, 1, 0.25, 0.25],
        [1.25, 1.25, 0.75, 0.75],
        [1.25, 1.25, 0.75, 0.5, 0.25],
        [1.25, 1.25, 0.75, 0.25, 0.25, 0.25],
        [1.25, 1.25, 0.5, 0.5, 0.5],
        [1.25, 1.25, 0.5, 0.5, 0.25, 0.25],
        [1.25, 1.25, 0.5, 0.25, 0.25, 0.25, 0.25],
        [1.25, 1.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1.25, 1, 1, 0.75],
        [1.25, 1, 1, 0.5, 0.25],
        [1.25, 1, 1, 0.25, 0.25, 0.25],
        [1.25, 1, 0.75, 0.75, 0.25],
        [1.25, 1, 0.75, 0.5, 0.5],
        [1.25, 1, 0.75, 0.5, 0.25, 0.25],
        [1.25, 1, 0.75, 0.25, 0.25, 0.25, 0.25],
        [1.25, 1, 0.5, 0.5, 0.5, 0.25],
        [1.25, 1, 0.5, 0.5, 0.25, 0.25, 0.25],
        [1.25, 1, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1.25, 1, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1.25, 0.75, 0.75, 0.75, 0.5],
        [1.25, 0.75, 0.75, 0.75, 0.25, 0.25],
        [1.25, 0.75, 0.75, 0.5, 0.5, 0.25],
        [1.25, 0.75, 0.75, 0.5, 0.25, 0.25, 0.25],
        [1.25, 0.75, 0.75, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1.25, 0.75, 0.5, 0.5, 0.5, 0.5],
        [1.25, 0.75, 0.5, 0.5, 0.5, 0.25, 0.25],
        [1.25, 0.75, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25],
        [1.25, 0.75, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1.25, 0.75, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1.25, 0.5, 0.5, 0.5, 0.5, 0.5, 0.25],
        [1.25, 0.5, 0.5, 0.5, 0.5, 0.25, 0.25, 0.25],
        [1.25, 0.5, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1.25, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1, 1, 1, 1],
        [1, 1, 1, 0.75, 0.25],
        [1, 1, 1, 0.5, 0.5],
        [1, 1, 1, 0.5, 0.25, 0.25],
        [1, 1, 1, 0.25, 0.25, 0.25, 0.25],
        [1, 1, 0.75, 0.75, 0.5],
        [1, 1, 0.75, 0.75, 0.25, 0.25],
        [1, 1, 0.75, 0.5, 0.5, 0.25],
        [1, 1, 0.75, 0.5, 0.25, 0.25, 0.25],
        [1, 1, 0.75, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1, 1, 0.5, 0.5, 0.5, 0.5],
        [1, 1, 0.5, 0.5, 0.5, 0.25, 0.25],
        [1, 1, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25],
        [1, 1, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1, 1, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1, 0.75, 0.75, 0.75, 0.75],
        [1, 0.75, 0.75, 0.75, 0.5, 0.25],
        [1, 0.75, 0.75, 0.75, 0.25, 0.25, 0.25],
        [1, 0.75, 0.75, 0.5, 0.5, 0.5],
        [1, 0.75, 0.75, 0.5, 0.5, 0.25, 0.25],
        [1, 0.75, 0.75, 0.5, 0.25, 0.25, 0.25, 0.25],
        [1, 0.75, 0.75, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1, 0.75, 0.5, 0.5, 0.5, 0.5, 0.25],
        [1, 0.75, 0.5, 0.5, 0.5, 0.25, 0.25, 0.25],
        [1, 0.75, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1, 0.75, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1, 0.75, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        [1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.25, 0.25],
        [1, 0.5, 0.5, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25],
        [1, 0.5, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [1, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [0.75, 0.75, 0.75, 0.75, 0.75, 0.25],
        [0.75, 0.75, 0.75, 0.75, 0.5, 0.5],
        [0.75, 0.75, 0.75, 0.75, 0.5, 0.25, 0.25],
        [0.75, 0.75, 0.75, 0.75, 0.25, 0.25, 0.25, 0.25],
        [0.75, 0.75, 0.75, 0.5, 0.5, 0.5, 0.25],
        [0.75, 0.75, 0.75, 0.5, 0.5, 0.25, 0.25, 0.25],
        [0.75, 0.75, 0.75, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25],
        [0.75, 0.75, 0.75, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [0.75, 0.75, 0.5, 0.5, 0.5, 0.5, 0.5],
        [0.75, 0.75, 0.5, 0.5, 0.5, 0.5, 0.25, 0.25],
        [0.75, 0.75, 0.5, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25],
        [0.75, 0.75, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [0.75, 0.75, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [0.75, 0.75, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [0.75, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.25],
        [0.75, 0.5, 0.5, 0.5, 0.5, 0.5, 0.25, 0.25, 0.25],
        [0.75, 0.5, 0.5, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25],
        [0.75, 0.5, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [0.75, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [0.75, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [0.75, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.25, 0.25],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [0.5, 0.5, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [0.5, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]
]

options1 = ['X', 'O']
options2 = ['X', 'O']
options3 = ['X', 'O']
options4 = ['X', 'O']
options5 = ['X', 'O']
options6 = ['X', 'O']
options7 = ['X', 'O']
options8 = ['X', 'O']
options9 = ['X', 'O']
options10 = ['X', 'O']
options11 = ['X', 'O']
options12 = ['X', 'O']
options13 = ['X', 'O']
options14 = ['X', 'O']
options15 = ['X', 'O']
options16 = ['X', 'O']

allRests = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

rests1 = ['Y']
rests2 = ['Y', 'Y']
rests3 = ['Y', 'Y', 'Y']
rests4 = ['Y', 'Y', 'Y', 'Y']
rests5 = ['Y', 'Y', 'Y', 'Y', 'Y']
rests6 = ['Y', 'Y', 'Y', 'Y', 'Y', 'Y']
rests7 = ['Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y']
rests8 = ['Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y']
rests9 = ['Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y']
rests10 = ['Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y']
rests11 = ['Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y']
rests12 = ['Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y']
rests13 = ['Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y']
rests14 = ['Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y']
rests15 = ['Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y']
rests16 = ['Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y']

for option1 in options1:
    rests1 = list(rests1)
    rests2 = list(rests2)
    rests3 = list(rests3)
    rests4 = list(rests4)
    rests5 = list(rests5)
    rests6 = list(rests6)
    rests7 = list(rests7)
    rests8 = list(rests8)
    rests9 = list(rests9)
    rests10 = list(rests10)
    rests11 = list(rests11)
    rests12 = list(rests12)
    rests13 = list(rests13)
    rests14 = list(rests14)
    rests15 = list(rests15)
    rests16 = list(rests16)
    rests1[0] = option1
    rests2[0] = option1
    rests3[0] = option1
    rests4[0] = option1
    rests5[0] = option1
    rests6[0] = option1
    rests7[0] = option1
    rests8[0] = option1
    rests9[0] = option1
    rests10[0] = option1
    rests11[0] = option1
    rests12[0] = option1
    rests13[0] = option1
    rests14[0] = option1
    rests15[0] = option1
    rests16[0] = option1
    allRests[0].append(rests1)
    for option2 in options2:
        rests2 = list(rests2)
        rests3 = list(rests3)
        rests4 = list(rests4)
        rests5 = list(rests5)
        rests6 = list(rests6)
        rests7 = list(rests7)
        rests8 = list(rests8)
        rests9 = list(rests9)
        rests10 = list(rests10)
        rests11 = list(rests11)
        rests12 = list(rests12)
        rests13 = list(rests13)
        rests14 = list(rests14)
        rests15 = list(rests15)
        rests16 = list(rests16)
        rests2[1] = option2
        rests3[1] = option2
        rests4[1] = option2
        rests5[1] = option2
        rests6[1] = option2
        rests7[1] = option2
        rests8[1] = option2
        rests9[1] = option2
        rests10[1] = option2
        rests11[1] = option2
        rests12[1] = option2
        rests13[1] = option2
        rests14[1] = option2
        rests15[1] = option2
        rests16[1] = option2
        allRests[1].append(rests2)
        for option3 in options3:
            rests3 = list(rests3)
            rests4 = list(rests4)
            rests5 = list(rests5)
            rests6 = list(rests6)
            rests7 = list(rests7)
            rests8 = list(rests8)
            rests9 = list(rests9)
            rests10 = list(rests10)
            rests11 = list(rests11)
            rests12 = list(rests12)
            rests13 = list(rests13)
            rests14 = list(rests14)
            rests15 = list(rests15)
            rests16 = list(rests16)
            rests3[2] = option3
            rests4[2] = option3
            rests5[2] = option3
            rests6[2] = option3
            rests7[2] = option3
            rests8[2] = option3
            rests9[2] = option3
            rests10[2] = option3
            rests11[2] = option3
            rests12[2] = option3
            rests13[2] = option3
            rests14[2] = option3
            rests15[2] = option3
            rests16[2] = option3
            allRests[2].append(rests3)
            for option4 in options4:
                rests4 = list(rests4)
                rests5 = list(rests5)
                rests6 = list(rests6)
                rests7 = list(rests7)
                rests8 = list(rests8)
                rests9 = list(rests9)
                rests10 = list(rests10)
                rests11 = list(rests11)
                rests12 = list(rests12)
                rests13 = list(rests13)
                rests14 = list(rests14)
                rests15 = list(rests15)
                rests16 = list(rests16)
                rests4[3] = option4
                rests5[3] = option4
                rests6[3] = option4
                rests7[3] = option4
                rests8[3] = option4
                rests9[3] = option4
                rests10[3] = option4
                rests11[3] = option4
                rests12[3] = option4
                rests13[3] = option4
                rests14[3] = option4
                rests15[3] = option4
                rests16[3] = option4
                allRests[3].append(rests4)
                for option5 in options5:
                    rests5 = list(rests5)
                    rests6 = list(rests6)
                    rests7 = list(rests7)
                    rests8 = list(rests8)
                    rests9 = list(rests9)
                    rests10 = list(rests10)
                    rests11 = list(rests11)
                    rests12 = list(rests12)
                    rests13 = list(rests13)
                    rests14 = list(rests14)
                    rests15 = list(rests15)
                    rests16 = list(rests16)
                    rests5[4] = option5
                    rests6[4] = option5
                    rests7[4] = option5
                    rests8[4] = option5
                    rests9[4] = option5
                    rests10[4] = option5
                    rests11[4] = option5
                    rests12[4] = option5
                    rests13[4] = option5
                    rests14[4] = option5
                    rests15[4] = option5
                    rests16[4] = option5
                    allRests[4].append(rests5)
                    for option6 in options6:
                        rests6 = list(rests6)
                        rests7 = list(rests7)
                        rests8 = list(rests8)
                        rests9 = list(rests9)
                        rests10 = list(rests10)
                        rests11 = list(rests11)
                        rests12 = list(rests12)
                        rests13 = list(rests13)
                        rests14 = list(rests14)
                        rests15 = list(rests15)
                        rests16 = list(rests16)
                        rests6[5] = option6
                        rests7[5] = option6
                        rests8[5] = option6
                        rests9[5] = option6
                        rests10[5] = option6
                        rests11[5] = option6
                        rests12[5] = option6
                        rests13[5] = option6
                        rests14[5] = option6
                        rests15[5] = option6
                        rests16[5] = option6
                        allRests[5].append(rests6)
                        for option7 in options7:
                            rests7 = list(rests7)
                            rests8 = list(rests8)
                            rests9 = list(rests9)
                            rests10 = list(rests10)
                            rests11 = list(rests11)
                            rests12 = list(rests12)
                            rests13 = list(rests13)
                            rests14 = list(rests14)
                            rests15 = list(rests15)
                            rests16 = list(rests16)
                            rests7[6] = option7
                            rests8[6] = option7
                            rests9[6] = option7
                            rests10[6] = option7
                            rests11[6] = option7
                            rests12[6] = option7
                            rests13[6] = option7
                            rests14[6] = option7
                            rests15[6] = option7
                            rests16[6] = option7
                            allRests[6].append(rests7)
                            for option8 in options8:
                                rests8 = list(rests8)
                                rests9 = list(rests9)
                                rests10 = list(rests10)
                                rests11 = list(rests11)
                                rests12 = list(rests12)
                                rests13 = list(rests13)
                                rests14 = list(rests14)
                                rests15 = list(rests15)
                                rests16 = list(rests16)
                                rests8[7] = option8
                                rests9[7] = option8
                                rests10[7] = option8
                                rests11[7] = option8
                                rests12[7] = option8
                                rests13[7] = option8
                                rests14[7] = option8
                                rests15[7] = option8
                                rests16[7] = option8
                                allRests[7].append(rests8)
                                for option9 in options9:
                                    rests9 = list(rests9)
                                    rests10 = list(rests10)
                                    rests11 = list(rests11)
                                    rests12 = list(rests12)
                                    rests13 = list(rests13)
                                    rests14 = list(rests14)
                                    rests15 = list(rests15)
                                    rests16 = list(rests16)
                                    rests9[8] = option9
                                    rests10[8] = option9
                                    rests11[8] = option9
                                    rests12[8] = option9
                                    rests13[8] = option9
                                    rests14[8] = option9
                                    rests15[8] = option9
                                    rests16[8] = option9
                                    allRests[8].append(rests9)
                                    for option10 in options10:
                                        rests10 = list(rests10)
                                        rests11 = list(rests11)
                                        rests12 = list(rests12)
                                        rests13 = list(rests13)
                                        rests14 = list(rests14)
                                        rests15 = list(rests15)
                                        rests16 = list(rests16)
                                        rests10[9] = option10
                                        rests11[9] = option10
                                        rests12[9] = option10
                                        rests13[9] = option10
                                        rests14[9] = option10
                                        rests15[9] = option10
                                        rests16[9] = option10
                                        allRests[9].append(rests10)
                                        for option11 in options11:
                                            rests11 = list(rests11)
                                            rests12 = list(rests12)
                                            rests13 = list(rests13)
                                            rests14 = list(rests14)
                                            rests15 = list(rests15)
                                            rests16 = list(rests16)
                                            rests11[10] = option11
                                            rests12[10] = option11
                                            rests13[10] = option11
                                            rests14[10] = option11
                                            rests15[10] = option11
                                            rests16[10] = option11
                                            allRests[10].append(rests11)
                                            for option12 in options12:
                                                rests12 = list(rests12)
                                                rests13 = list(rests13)
                                                rests14 = list(rests14)
                                                rests15 = list(rests15)
                                                rests16 = list(rests16)
                                                rests12[11] = option12
                                                rests13[11] = option12
                                                rests14[11] = option12
                                                rests15[11] = option12
                                                rests16[11] = option12
                                                allRests[11].append(rests12)
                                                for option13 in options13:
                                                    rests13 = list(rests13)
                                                    rests14 = list(rests14)
                                                    rests15 = list(rests15)
                                                    rests16 = list(rests16)
                                                    rests13[12] = option13
                                                    rests14[12] = option13
                                                    rests15[12] = option13
                                                    rests16[12] = option13
                                                    allRests[12].append(rests13)
                                                    for option14 in options14:
                                                        rests14 = list(rests14)
                                                        rests15 = list(rests15)
                                                        rests16 = list(rests16)
                                                        rests14[13] = option14
                                                        rests15[13] = option14
                                                        rests16[13] = option14
                                                        allRests[13].append(rests14)
                                                        for option15 in options15:
                                                            rests15 = list(rests15)
                                                            rests16 = list(rests16)
                                                            rests15[14] = option15
                                                            rests16[14] = option15
                                                            allRests[14].append(rests15)
                                                            for option16 in options16:
                                                                rests16 = list(rests16)
                                                                rests16[15] = option16
                                                                allRests[15].append(rests16)

del options1
del options2
del options3
del options4
del options5
del options6
del options7
del options8
del options9
del options10
del options11
del options12
del options13
del options14
del options15
del options16
del rests1
del rests2
del rests3
del rests4
del rests5
del rests6
del rests7
del rests8
del rests9
del rests10
del rests11
del rests12
del rests13
del rests14
del rests15
del rests16

countList1 = []
countList2 = []
countList3 = []
countList4 = []
countList5 = []
countList6 = []
countList7 = []
countList8 = []
countList9 = []
countList10 = []
countList11 = []
countList12 = []
countList13 = []
countList14 = []
countList15 = []
countList16 = []
for count in fullCountsList:
    match len(count):
        case 1:
            countList1.append(count)
        case 2:
            countList2.append(count)
        case 3:
            countList3.append(count)
        case 4:
            countList4.append(count)
        case 5:
            countList5.append(count)
        case 6:
            countList6.append(count)
        case 7:
            countList7.append(count)
        case 8:
            countList8.append(count)
        case 9:
            countList9.append(count)
        case 10:
            countList10.append(count)
        case 11:
            countList11.append(count)
        case 12:
            countList12.append(count)
        case 13:
            countList13.append(count)
        case 14:
            countList14.append(count)
        case 15:
            countList15.append(count)
        case 16:
            countList16.append(count)

fullCountsList = []
fullCountsList.append(countList1)
fullCountsList.append(countList2)
fullCountsList.append(countList3)
fullCountsList.append(countList4)
fullCountsList.append(countList5)
fullCountsList.append(countList6)
fullCountsList.append(countList7)
fullCountsList.append(countList8)
fullCountsList.append(countList9)
fullCountsList.append(countList10)
fullCountsList.append(countList11)
fullCountsList.append(countList12)
fullCountsList.append(countList13)
fullCountsList.append(countList14)
fullCountsList.append(countList15)
fullCountsList.append(countList16)
del countList1
del countList2
del countList3
del countList4
del countList5
del countList6
del countList7
del countList8
del countList9
del countList10
del countList11
del countList12
del countList13
del countList14
del countList15
del countList16

fileList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
if __name__ == "__main__":
    for index, fileNumber in enumerate(fileList):
        if not os.path.exists(f"Rythms{fileNumber}.txt"):
            with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:

                print(1)

                if fileNumber < 14:
                    countsList = fullCountsList[index]
                    countResultsPackaged = list(pool.map(permutateValueList, countsList))
                    del countsList
                    countResults = unpackageList(countResultsPackaged)
                    del countResultsPackaged
                else:
                    match fileNumber:
                        case 14:
                            countResults = [
                                [0.75, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.75, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.75, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.75, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.75, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.75, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.75, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.75, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.75, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.75, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.75, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.75, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.75, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.75],
                                [0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.5, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.5, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.5, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.5, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25],
                                [0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25],
                                [0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25],
                                [0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25],
                                [0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5],
                                [0.25, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.5, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.5, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.5, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25],
                                [0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25],
                                [0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25],
                                [0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5],
                                [0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.5, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.5, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25],
                                [0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25],
                                [0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5],
                                [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.5, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25],
                                [0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5],
                                [0.25, 0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.5, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.5, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.5, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.5],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.5, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.5, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.5],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.5, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.5],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.5],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5]
                            ]
                        
                        case 15:
                            countResults = [
                                [0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25],
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5]
                            ]

                        case 16:
                            countResults = [
                                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]
                            ]

                print(2)

                restResults = allRests[index]

                restAndCountsTouples = []
                for count in countResults:
                    for rest in restResults:
                        restAndCountsTouples.append((count, rest))
                del countResults
                del restResults

                print(3)

                rythmResultsPackaged = list(pool.map(combineRestsAndCounts, restAndCountsTouples))

                del restAndCountsTouples

                print(4)

                rythmResults = removeDuplicates(rythmResultsPackaged, 1)

                del rythmResultsPackaged

                print(5)

                rythmList = list(pool.map(combineRests, rythmResults))

                del rythmResults

                print(6)

                finalRythmList = removeDuplicates(rythmList, 0)

                del rythmList

                print(7)

                with open(f"Rythms{fileNumber}.txt", "w") as file:
                    for rythm in finalRythmList:
                        file.write(str(rythm))
                print(f"Rythms{fileNumber}" + " Done")

    del fullCountsList

    fullRythmsList = []
    for fileNumber in fileList:
        with open(f"Rythms{fileNumber}.txt", "r") as file:
            rythmsList = file.readlines()
            for rythm in rythmsList:
                fullRythmsList.append(rythm)
            fullRythmsList = list(set(fullRythmsList))
        with open("Rythms.txt", "w") as file:
            for rythm in fullRythmsList:
                file.write(str(rythm))
        print(f"Rythms file written {fileNumber} time(s)")
        os.remove(f"Rythms{fileNumber}.txt")
        print(f"Rythms{fileNumber}.txt deleted")
        
    print("Task Completed")
