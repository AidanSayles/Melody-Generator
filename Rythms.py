import os
import sys
import ast
import linecache
import random
import pygame

directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(directory)

pygame.mixer.init()
pygame.mixer.set_num_channels(32)  # Increase the number of channels

clock = pygame.time.Clock()

WIDTH, HEIGHT = 852, 602
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Melody Generator")

BPM = 90
beatLength = 16

PRX = 0
PRY = 0
PianoRoll = pygame.transform.scale(pygame.image.load("images/PianoRoll.png"), (852, 602))
PRLetters = pygame.transform.scale(pygame.image.load("images/PRLetters.png"), (850, 600))
PRNote = pygame.transform.scale(pygame.image.load("images/Note.png"), (48, 48))
PRInactiveLetter = pygame.transform.scale(pygame.image.load("images/InactiveLetter.png"), (48, 48))
letterCollidePoints = [
    pygame.Rect(PRX + 1, PRY + 1, 48, 48),
    pygame.Rect(PRX + 1, PRY + 51, 48, 48),
    pygame.Rect(PRX + 1, PRY + 101, 48, 48),
    pygame.Rect(PRX + 1, PRY + 151, 48, 48),
    pygame.Rect(PRX + 1, PRY + 201, 48, 48),
    pygame.Rect(PRX + 1, PRY + 251, 48, 48),
    pygame.Rect(PRX + 1, PRY + 301, 48, 48),
    pygame.Rect(PRX + 1, PRY + 351, 48, 48),
    pygame.Rect(PRX + 1, PRY + 401, 48, 48),
    pygame.Rect(PRX + 1, PRY + 451, 48, 48),
    pygame.Rect(PRX + 1, PRY + 501, 48, 48),
    pygame.Rect(PRX + 1, PRY + 551, 48, 48)
]

#lowercase = natural
#uppercase = sharp
allNotes = ["G", "g", "F", "f", "e", "D", "d", "C", "c", "b", "A", "a"]
inactiveNotes  = []
noteHeights = {"G": 2, "g": 52, "F": 102, "f": 152, "e": 202, "D": 252, "d": 302, "C": 352, "c": 402, "b": 452, "A": 502, "a": 552}

def createRythm():
    filePick = random.randint(1, 4)
    if filePick == 1:
        rythm = list(ast.literal_eval(linecache.getline("Rythms1.txt", random.randint(1, 962634)).strip()))
    elif filePick == 2:
        rythm = list(ast.literal_eval(linecache.getline("Rythms2.txt", random.randint(1, 962633)).strip()))
    elif filePick == 3:
        rythm = list(ast.literal_eval(linecache.getline("Rythms3.txt", random.randint(1, 962633)).strip()))
    else:
        rythm = list(ast.literal_eval(linecache.getline("Rythms4.txt", random.randint(1, 962633)).strip()))
    rythm = distributeRests(rythm)
    return rythm

def distributeRests(rythm):
    newRythm = []
    for beat in rythm:
        if beat[0] != "O":
            newRythm.append(beat)
        else:
            for i in range(int(float(beat[1:]) / 0.25)):
                newRythm.append("O0.25")
    return newRythm


def createMelody(rythm):
    melody = []
    for beat in rythm:
        if beat[0] == "X":
            melody.append(notes[random.randint(0, (len(notes) - 1))] + beat[1:])
        else:
            melody.append(beat)
    return melody

def createSounds(melody):
    soundList = []
    for note in melody:
        if note[0] != "O":
            if note[0] in ["A", "C", "D", "F", "G"]:
                sound = "sounds/" + note[0] + "#" + note[1:] + ".mp3"
            else:
                sound = "sounds/" + note[0].upper() + note[1:] + ".mp3"
            i = pygame.mixer.Sound(sound)
            soundList.append(i)
    return (soundList)

def createPRNotes(melody):
    PRNotes = []
    x = 52
    for note in melody:
        width = note[1:].strip()
        width = ((float(width) * 200) - 2)
        if note[0] != "O":
            y = noteHeights[note[0]]
            PRNotes.append((pygame.transform.scale(PRNote, (width, 48)), (x, y)))
        x += width + 2
    return PRNotes

def createNoteCollidePoints(PRNotes):
    noteCollidePoints = []
    for info in PRNotes:
        surface, position = info
        width, height = surface.get_size()
        x, y = position
        noteCollidePoint = pygame.Rect(x, y, width, height)
        noteCollidePoints.append(noteCollidePoint)
    return noteCollidePoints

def createNoteIndexDictionary(rythm):
    noteIndexDict = {}
    noteCount = 0
    for index, beat in enumerate(rythm):
        if beat[0] == "X":
            noteIndexDict[noteCount] = index
            noteCount += 1
    return noteIndexDict

def createRestMap(rythm):
    restMap = []
    i = 0
    for index, beat in enumerate(rythm):
        if beat == "O0.25":
            restMap.append("O")
            i += 1
        else:
            xTimes = int(float(beat[1:]) / 0.25)
            for i in range(xTimes):
                restMap.append("X")
                i += 1
    return restMap

def createRestMapDict(rythm):
    restMapDict = {}
    noteCount = 0
    for index, beat in enumerate(rythm):
        times = int(float(beat[1:]) / 0.25)
        for i in range(times):
            restMapDict[noteCount] = index
            noteCount += 1
    return restMapDict

def displayPianoRoll():
    WIN.blit(PianoRoll, (PRX, PRY))
    for note in inactiveNotes:
        WIN.blit(PRInactiveLetter, ((PRX + 2), noteHeights[note]))
    WIN.blit(PRLetters, ((PRX + 1), (PRY + 1)))

def displayPRNotes(PRNotes):
    for info in PRNotes:
        note, position = info
        WIN.blit(note, position)

def displayCurrentNote(info):
    note, position = info
    PRCurrentNote = pygame.transform.scale(pygame.image.load("images/PlayNote.png"), note.get_size())
    WIN.blit(PRCurrentNote, position)

def displaySelectedNote(info):
    note, position = info
    PRSelectedNote = pygame.transform.scale(pygame.image.load("images/SelectNote.png"), note.get_size())
    WIN.blit(PRSelectedNote, position)

def display(PRNotes, specialNote, noteType):
    displayPianoRoll()
    displayPRNotes(PRNotes)
    if noteType == "current":
        displayCurrentNote(specialNote)
    elif noteType == "selected":
        displaySelectedNote(specialNote)
    pygame.display.update()

def newAll():
    rythm = createRythm()
    restMap = createRestMap(rythm)
    restMapDict = createRestMapDict(rythm)
    melody = createMelody(rythm)
    noteIndexDict = createNoteIndexDictionary(rythm)
    soundList = createSounds(melody)
    PRNotes = createPRNotes(melody)
    noteCollidePoints = createNoteCollidePoints(PRNotes)
    display(PRNotes, "None", "None")
    return (rythm, restMap, restMapDict, melody, noteIndexDict, soundList, PRNotes, noteCollidePoints)

def newMelody(rythm):
    melody = createMelody(rythm)
    noteIndexDict = createNoteIndexDictionary(rythm)
    soundList = createSounds(melody)
    PRNotes = createPRNotes(melody)
    noteCollidePoints = createNoteCollidePoints(PRNotes)
    display(PRNotes, "None", "None")
    return (melody, noteIndexDict, soundList, PRNotes, noteCollidePoints)

def update(rythm, melody):
    restMap = createRestMap(rythm)
    restMapDict = createRestMapDict(rythm)
    noteIndexDict = createNoteIndexDictionary(rythm)
    soundList = createSounds(melody)
    PRNotes = createPRNotes(melody)
    noteCollidePoints = createNoteCollidePoints(PRNotes)
    return (restMap, restMapDict, noteIndexDict, soundList, PRNotes, noteCollidePoints)

def switch(index1, index2, myList):
    temp = myList[index1]
    myList[index1] = myList[index2]
    myList[index2] = temp
    return myList

def getAdjacentRests(index, myList, direction):
    rests = 0
    note = False
    if direction == "+":
        end = len(myList) - 1
        if index != end:
            index += 1
        else:
            note = True
        while not note:
            if myList[index][0] == "O":
                rests += 1
                if index != end:
                    index += 1
                else:
                    note = False
                    break
            else:
                note = False
                break
    elif direction == "-":
        if index != 0:
            index -= 1
        else:
            note = True
        while not note:
            if myList[index][0] == "O":
                rests += 1
                if index != 0:
                    index -= 1
                else:
                    note = False
                    break
            else:
                note = False
                break
    return rests



def main():

    global notes
    notes = ["G", "g", "F", "f", "e", "D", "d", "C", "c", "b", "A", "a"]

    run = True

    kick = pygame.mixer.Sound("sounds/kick.mp3")
    metronomeTick = pygame.mixer.Sound("sounds/metronome.mp3")

    rythm, restMap, restMapDict, melody, noteIndexDict, soundList, PRNotes, noteCollidePoints = newAll()

    play = False

    metronome = False

    tune = True

    coolDown = 0

    selectedNote = None

    while run:
        clock.tick(60)
        for event in pygame.event.get():

            # quitting
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                mouse = pygame.mouse.get_pos()
                for index, letterCollidePoint in enumerate(letterCollidePoints):
                    if letterCollidePoint.collidepoint(mouse):
                        if allNotes[index] in notes:
                            inactiveNotes.append(allNotes[index])
                            notes = allNotes.copy()
                            for note in inactiveNotes:
                                if note in notes:
                                    notes.remove(note)
                        else:
                            inactiveNotes.remove(allNotes[index])
                            notes = allNotes.copy()
                            for note in inactiveNotes:
                                if note in notes:
                                    notes.remove(note)
                        break
                for index, noteCollidePoint in enumerate(noteCollidePoints):
                    if noteCollidePoint.collidepoint(mouse):
                        if selectedNote == index:
                            selectedNote = None
                        else:
                            selectedNote = index
                        break
                if selectedNote != None:
                    display(PRNotes, PRNotes[selectedNote], "selected")
                else:
                    display(PRNotes, None, None)
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT and selectedNote != None:
                mouse = pygame.mouse.get_pos()
                for index, noteCollidePoint in enumerate(noteCollidePoints):
                    if noteCollidePoint.collidepoint(mouse):
                        if selectedNote != index:
                            rythm = switch(noteIndexDict[index], noteIndexDict[selectedNote], rythm)
                            melody = switch(noteIndexDict[index], noteIndexDict[selectedNote], melody)
                            restMap, restMapDict, noteIndexDict, soundList, PRNotes, noteCollidePoints = update(rythm, melody)
                            selectedNote = None
                        break
                display(PRNotes, None, None)

        keys = pygame.key.get_pressed()
        if coolDown == 0:
            if keys[pygame.K_SPACE]:
                play = True
                coolDown = 24
                selectedNote = None
                melodyIndex = 0
                soundIndex = 0
                noteTime = 0
                beatTime = 0

            if keys[pygame.K_n]:
                rythm, restMap, restMapDict, melody, noteIndexDict, soundList, PRNotes, noteCollidePoints = newAll()
                coolDown = 30
                display(PRNotes, None, None)

            if keys[pygame.K_m]:
                melody, noteIndexDict, soundList, PRNotes, noteCollidePoints = newMelody(rythm)
                coolDown = 30
                display(PRNotes, None, None)

            if keys[pygame.K_t]:
                tune = not tune
                coolDown = 30

            if keys[pygame.K_b]:
                metronome = not metronome
                coolDown = 30

            if keys[pygame.K_c]:
                mouse = pygame.mouse.get_pos()
                x, y = mouse
                beatNum = int((x - 1) / 50) - 1
                if -1 < beatNum < 16 and restMap[beatNum] == "O":
                    noteNum = int((y - 1) / 50)
                    if noteNum < len(allNotes):
                        newNote = allNotes[noteNum]
                        if keys[pygame.K_LCTRL]:
                            deleteNum = 1
                            deleteNum += getAdjacentRests(restMapDict[beatNum], rythm, "+")
                            deleteNum += getAdjacentRests(restMapDict[beatNum], rythm, "-")
                            deleteIndex = restMapDict[beatNum] - getAdjacentRests(restMapDict[beatNum], rythm, "-")
                            for i in range(deleteNum):
                                del rythm[deleteIndex]
                                print(f"rythm {rythm}")
                                del melody[deleteIndex]
                            newNote = newNote + str(deleteNum * 0.25).rstrip('0').rstrip('.')
                            rythm.insert(deleteIndex, ("X" + newNote[1:]))
                            melody.insert(deleteIndex, newNote)
                        else:
                            rythm[restMapDict[beatNum]] = "X0.25"
                            melody[restMapDict[beatNum]] = newNote + "0.25"
                restMap, restMapDict, noteIndexDict, soundList, PRNotes, noteCollidePoints = update(rythm, melody)
                coolDown = 30
                display(PRNotes, None, None)
            
            if selectedNote != None:
                if keys[pygame.K_DELETE]:
                    rythm[noteIndexDict[selectedNote]] = "O" + rythm[noteIndexDict[selectedNote]][1:]
                    rythm = distributeRests(rythm)
                    melody[noteIndexDict[selectedNote]] = "O" + melody[noteIndexDict[selectedNote]][1:]
                    melody = distributeRests(melody)
                    restMap, restMapDict, noteIndexDict, soundList, PRNotes, noteCollidePoints = update(rythm, melody)
                    selectedNote = None
                    coolDown = 30
                    display(PRNotes, None, None)

                if keys[pygame.K_BACKSPACE] and rythm[noteIndexDict[selectedNote]][1:] != "0.25":
                    if keys[pygame.K_LCTRL]:
                        rests = int(float(rythm[noteIndexDict[selectedNote]][1:]) / 0.25) - 1
                        rythm[noteIndexDict[selectedNote]] = "X0.25"
                        melody[noteIndexDict[selectedNote]] = melody[noteIndexDict[selectedNote]][0] + "0.25"
                        for i in range(rests):
                            rythm.insert((noteIndexDict[selectedNote] + 1), "O0.25")
                            melody.insert((noteIndexDict[selectedNote] + 1), "O0.25")
                    else:
                        rythm[noteIndexDict[selectedNote]] = rythm[noteIndexDict[selectedNote]][0] + str(float(rythm[noteIndexDict[selectedNote]][1:]) - 0.25).rstrip('0').rstrip('.')
                        rythm.insert((noteIndexDict[selectedNote] + 1), "O0.25")
                        melody[noteIndexDict[selectedNote]] = melody[noteIndexDict[selectedNote]][0] + str(float(melody[noteIndexDict[selectedNote]][1:]) - 0.25).rstrip('0').rstrip('.')
                        melody.insert((noteIndexDict[selectedNote] + 1), "O0.25")
                    restMap, restMapDict, noteIndexDict, soundList, PRNotes, noteCollidePoints = update(rythm, melody)
                    coolDown = 30
                    display(PRNotes, PRNotes[selectedNote], "selected")

                if keys[pygame.K_UP] and melody[noteIndexDict[selectedNote]][0] != allNotes[0]:
                    if keys[pygame.K_LCTRL]:
                        melody[noteIndexDict[selectedNote]] = allNotes[0] + melody[noteIndexDict[selectedNote]][1:]
                    else:
                        melody[noteIndexDict[selectedNote]] = notes[notes.index(melody[noteIndexDict[selectedNote]][0]) - 1]+ melody[noteIndexDict[selectedNote]][1:]
                    restMap, restMapDict, noteIndexDict, soundList, PRNotes, noteCollidePoints = update(rythm, melody)
                    coolDown = 30
                    display(PRNotes, PRNotes[selectedNote], "selected")

                if keys[pygame.K_DOWN] and melody[noteIndexDict[selectedNote]][0] != allNotes[-1]:
                    if keys[pygame.K_LCTRL]:
                        melody[noteIndexDict[selectedNote]] = allNotes[-1] + melody[noteIndexDict[selectedNote]][1:]
                    else:
                        melody[noteIndexDict[selectedNote]] = notes[notes.index(melody[noteIndexDict[selectedNote]][0]) + 1]+ melody[noteIndexDict[selectedNote]][1:]
                    restMap, restMapDict, noteIndexDict, soundList, PRNotes, noteCollidePoints = update(rythm, melody)
                    coolDown = 30
                    display(PRNotes, PRNotes[selectedNote], "selected")

                if keys[pygame.K_RIGHT] and noteIndexDict[selectedNote] != (len(rythm) - 1):
                    if keys[pygame.K_LCTRL]:
                        if keys[pygame.K_LSHIFT]:
                            temp = rythm[noteIndexDict[selectedNote]]
                            del rythm[noteIndexDict[selectedNote]]
                            rythm.append(temp)
                            temp = melody[noteIndexDict[selectedNote]]
                            del melody[noteIndexDict[selectedNote]]
                            melody.append(temp)
                            selectedNote = len(noteCollidePoints) - 1
                        elif rythm[noteIndexDict[selectedNote] + 1] == "O0.25":
                            rests = getAdjacentRests(noteIndexDict[selectedNote], rythm, "+")
                            rythm = switch(noteIndexDict[selectedNote], (noteIndexDict[selectedNote] + rests), rythm)
                            melody = switch(noteIndexDict[selectedNote], (noteIndexDict[selectedNote] + rests), melody)
                    else:
                        oldIndex = noteIndexDict[selectedNote]
                        rythm = switch(noteIndexDict[selectedNote], (noteIndexDict[selectedNote] + 1), rythm)
                        melody = switch(noteIndexDict[selectedNote], (noteIndexDict[selectedNote] + 1), melody)
                        if rythm[oldIndex][0] !="O":
                            selectedNote += 1
                    restMap, restMapDict, noteIndexDict, soundList, PRNotes, noteCollidePoints = update(rythm, melody)
                    coolDown = 30
                    display(PRNotes, PRNotes[selectedNote], "selected")

                if keys[pygame.K_LEFT] and noteIndexDict[selectedNote] != 0:
                    if keys[pygame.K_LCTRL]:
                        if keys[pygame.K_LSHIFT]:
                            temp = rythm[noteIndexDict[selectedNote]]
                            del rythm[noteIndexDict[selectedNote]]
                            rythm.insert(0, temp)
                            temp = melody[noteIndexDict[selectedNote]]
                            del melody[noteIndexDict[selectedNote]]
                            melody.insert(0, temp)
                            selectedNote = 0
                        elif rythm[noteIndexDict[selectedNote] - 1] == "O0.25":
                            rests = getAdjacentRests(noteIndexDict[selectedNote], rythm, "-")
                            rythm = switch(noteIndexDict[selectedNote], (noteIndexDict[selectedNote] - rests), rythm)
                            melody = switch(noteIndexDict[selectedNote], (noteIndexDict[selectedNote] - rests), melody)
                    else:
                        oldIndex = noteIndexDict[selectedNote]
                        rythm = switch(noteIndexDict[selectedNote], (noteIndexDict[selectedNote] - 1), rythm)
                        melody = switch(noteIndexDict[selectedNote], (noteIndexDict[selectedNote] - 1), melody)
                        if rythm[oldIndex][0] !="O":
                            selectedNote -= 1
                    restMap, restMapDict, noteIndexDict, soundList, PRNotes, noteCollidePoints = update(rythm, melody)
                    coolDown = 30
                    display(PRNotes, PRNotes[selectedNote], "selected")

                if keys[pygame.K_d] and rythm[noteIndexDict[selectedNote] + 1][0] == "O":
                    if keys[pygame.K_LCTRL]:
                        rests = getAdjacentRests(noteIndexDict[selectedNote], rythm, "+")
                        rythm[noteIndexDict[selectedNote]] = rythm[noteIndexDict[selectedNote]][0] + str(float(rythm[noteIndexDict[selectedNote]][1:]) + (0.25 * rests)).rstrip('0').rstrip('.')
                        melody[noteIndexDict[selectedNote]] = melody[noteIndexDict[selectedNote]][0] + str(float(melody[noteIndexDict[selectedNote]][1:]) + (0.25 * rests)).rstrip('0').rstrip('.')
                        for i in range(rests):
                            del rythm[noteIndexDict[selectedNote] + 1]
                            del melody[noteIndexDict[selectedNote] + 1]
                    else:
                        rythm[noteIndexDict[selectedNote]] = rythm[noteIndexDict[selectedNote]][0] + str(float(rythm[noteIndexDict[selectedNote]][1:]) + 0.25).rstrip('0').rstrip('.')
                        del rythm[noteIndexDict[selectedNote] + 1]
                        melody[noteIndexDict[selectedNote]] = melody[noteIndexDict[selectedNote]][0] + str(float(melody[noteIndexDict[selectedNote]][1:]) + 0.25).rstrip('0').rstrip('.')
                        del melody[noteIndexDict[selectedNote] + 1]
                    restMap, restMapDict, noteIndexDict, soundList, PRNotes, noteCollidePoints = update(rythm, melody)
                    coolDown = 30
                    display(PRNotes, PRNotes[selectedNote], "selected")

                if keys[pygame.K_a] and rythm[noteIndexDict[selectedNote] - 1][0] == "O":
                    if keys[pygame.K_LCTRL]:
                        rests = getAdjacentRests(noteIndexDict[selectedNote], rythm, "-")
                        rythm[noteIndexDict[selectedNote]] = rythm[noteIndexDict[selectedNote]][0] + str(float(rythm[noteIndexDict[selectedNote]][1:]) + (0.25 * rests)).rstrip('0').rstrip('.')
                        melody[noteIndexDict[selectedNote]] = melody[noteIndexDict[selectedNote]][0] + str(float(melody[noteIndexDict[selectedNote]][1:]) + (0.25 * rests)).rstrip('0').rstrip('.')
                        for i in range(rests):
                            del rythm[noteIndexDict[selectedNote] - (i + 1)]
                            del melody[noteIndexDict[selectedNote] - (i + 1)]
                    else:
                        rythm[noteIndexDict[selectedNote]] = rythm[noteIndexDict[selectedNote]][0] + str(float(rythm[noteIndexDict[selectedNote]][1:]) + 0.25).rstrip('0').rstrip('.')
                        del rythm[noteIndexDict[selectedNote] - 1]
                        melody[noteIndexDict[selectedNote]] = melody[noteIndexDict[selectedNote]][0] + str(float(melody[noteIndexDict[selectedNote]][1:]) + 0.25).rstrip('0').rstrip('.')
                        del melody[noteIndexDict[selectedNote] - 1]
                    restMap, restMapDict, noteIndexDict, soundList, PRNotes, noteCollidePoints = update(rythm, melody)
                    coolDown = 30
                    display(PRNotes, PRNotes[selectedNote], "selected")

                            
                        





        while play:
            clock.tick(24)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and coolDown == 0:
                play = False
                coolDown = 30
                display(PRNotes, None, None)
                break
            if keys[pygame.K_t] and coolDown == 0:
                tune = not tune
                coolDown = 24
            if keys[pygame.K_b] and coolDown == 0:
                metronome = not metronome
                coolDown = 24

            if beatTime == 0:
                beatTime = beatLength
                if metronome:
                    metronomeTick.play()

            if noteTime == 0:
                display(PRNotes, None, None)
                noteTime = int(float(melody[melodyIndex][1:].strip())  * beatLength)
                if melody[melodyIndex][0] != "O":
                    if tune:
                        displayCurrentNote(PRNotes[soundIndex])
                        pygame.display.update()
                        soundList[soundIndex].play()
                        soundIndex += 1
                        if soundIndex == len(soundList):
                            soundIndex = 0
                    else:
                        kick.play()
                melodyIndex += 1
                if melodyIndex == len(melody):
                    melodyIndex = 0

            beatTime -= 1
            noteTime -= 1
            if coolDown > 0:
                coolDown -= 1
        if coolDown > 0:
            coolDown -= 1

    pygame.quit()

main()