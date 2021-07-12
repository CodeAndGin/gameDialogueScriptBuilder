# Script Writer for Lughnasadh - TODO: including pronoun choice markers
# Diarmaid Brennan - 2021
#
# Version 0.2

### IMPORTS ###

import PySimpleGUI as gui   # Using PySimpleGUI for making the GUI
import os.path              #os.path for reading and writing to files
import json                 #json to write the data into a JSON file
#from xml.etree.ElementTree import Element,tostring #XML writing
#import csv

### IMPORTS END ###

### CLASSES ###

class Actor:

    # Class initialisation. Gives the object its character name, and 2 empty
    # Lists to store each line of dialogue that the character says as well as
    # their places in the script

    def __init__(self, n = ""):
        self.name = n
        self.dialogue = []
        self.indices = []

    # When called - adds a new line of dialogue and its place in the conversation
    # to the correct Lists
    def add_dialogue(self, d, i):
        if i not in self.indices:
            self.dialogue.append(d)
            self.indices.append(i)
        else:
            self.dialogue[self.indices.index(i)] = d

    # Returns the name of the character stored in a given object
    def get_name(self):
        return self.name

    # Returns the List of lines of dialogue
    def get_dialogue(self):
        return self.dialogue

    # Returns the List of indices for where each line of dialogue goes
    def get_indices(self):
        return self.indices

### CLASSES END ###


### GLOBAL VARIABLES ###

gui.theme("LightGrey1")

actors = [] # List of each character in the conversation
index = 0 # Keeps track of how many lines and their correct places
tempindex = 0
names = []
filename = "" # For naming dialogue files
layout = [] # List for GUI layout
windowTitle = "Game Dialogue Script Builder" # str for window windowTitle

script = []

nameCurrent = ""
dialogueCurrentLine = ""

textInputLayout =      [[gui.Text("Character name:")],
                        [gui.InputText(nameCurrent, size=(30,1),enable_events=True, k="_NAME_INPUT_"), gui.DropDown(names, size=(20,1), enable_events=True, k="_NAME_LIST_")],
                        [gui.Text("Line(s) of dialogue:")],
                        [gui.Multiline(dialogueCurrentLine, autoscroll=True, size=(50,5), auto_refresh=True, enable_events=True, key="_DIALOG_INPUT_")],
                        [gui.Button("Confirm", key="_DIALOG_ENTERED_"), gui.Button("New", key= "_INPUT_RESET_")]]

outputLayout =         [[gui.Listbox(values=[],enable_events=True,size=(50,30),k="_SCRIPT_LAYOUT_")],
                        [gui.Text("Filename (no need to include the filetype ending):")],
                        [gui.InputText(filename, enable_events=True, k="FILENAME")],
                        [gui.Button("Edit Selected", k= "EDIT"), gui.Button("Save to JSON",k="PJSON")]]

layout= [[gui.Column(textInputLayout)],
         [gui.HorizontalSeparator()],
         [gui.Column(outputLayout)]]
### GLOBAL VARIABLES END ###


### FUNCTIONS ###

## GUI USABILITY AND TEXT PARSING ##

def resetInputBoxes(name, dialogue):
    window["_NAME_INPUT_"].update(name)
    window["_DIALOG_INPUT_"].update(dialogue)

def updateScript(i):
    for a in actors:
        if i in a.indices:
            sl = a.name + ": " + a.dialogue[a.indices.index(i)]
            try:
                if script[i] == sl:
                    break
            except:
                pass
            if i == index:
                script.append(sl)
            else:
                script[i] = sl
            break
    print(script)
    window["_SCRIPT_LAYOUT_"].update(script)

def updateNames():
    names = []
    for a in actors:
        names.append([a.name])
    window["_NAME_LIST_"].update(names)

def fixActorList(i, correct):
    for a in actors:
        if i in a.indices:
            if a.name != correct.name:
                a.dialogue.pop(a.indices.index(i))
                a.indices.pop(a.indices.index(i))
                if len(a.dialogue) == 0:
                    actors.pop(actors.index(a))


## GUI USABILITY AND TEXT PARSING ENDS ##

## JSON ##
# JSON FUNCTIONS PURPOSE: To export the dialogue instance in the form {actors:
# [{actordata1}, {actordata2}, ...]}

# Converts an instance of the Actor class (a) to a dictionary for easy conversion to JSON
def convert_actor_to_dict_for_JSON(a):
    dictionary = {}

    dictionary["name"] = a.get_name()
    dictionary["dialogue"] = a.get_dialogue()
    dictionary["indices"] = a.get_indices()

    return dictionary

# Takes the current total script and converts and dumps to JSON
def print_to_json():
    actordicts = []
    for actor in actors:
        actordicts.append(convert_actor_to_dict_for_JSON(actor))

    # Checks for filename already exists - appends number.
    # eg a.json exists, names filename a(1).json
    fn = filename
    try:
        if os.path.exists(fn + ".json"):
            a = 1
            while True:
                if os.path.exists(fn + "(" + str(a) + ").json"):
                    a += 1
                    continue
                else:
                    fn = fn + "(" + str(a) + ").json"
                    break
        else:
            fn+=".json"
    except:
        print("JSON PRINT ERROR")
        return

    d = {}
    d["actors"] = actordicts

    with open (fn, "w+") as f:
        json.dump(d, f, ensure_ascii=False)
## JSON END ##

## CSV ##

# TODO: Write CSV implementation

## CSV END ##

## XML ##

# TODO: Write XML implementation

## XML END ##

### FUNCTIONS END ###

### MAIN PROGRAM LOGIC ###

## EVENT LOOP ##

window = gui.Window(windowTitle, layout, margins=(20,20))

while True:
    event, values = window.read()

    if event == gui.WIN_CLOSED:
        break

    if event == "_INPUT_RESET_":
        resetInputBoxes("","")
        nameCurrent = ""
        dialogueCurrentLine = ""
        tempindex = index

    if event == "EDIT":
        n = ""
        d = ""
        tempindex = script.index(values["_SCRIPT_LAYOUT_"][0])
        for a in actors:
            if tempindex in a.indices:
                n = a.name
                d = a.dialogue[a.indices.index(tempindex)]
        nameCurrent=n
        dialogueCurrentLine=d
        window["_NAME_INPUT_"].update(n)
        window["_DIALOG_INPUT_"].update(d)

    if event == "_NAME_INPUT_":
        nameCurrent = values["_NAME_INPUT_"]

    if event == "_DIALOG_INPUT_":
        dialogueCurrentLine = values["_DIALOG_INPUT_"]

    if event == "FILENAME":
        filename = values["FILENAME"]

    if event == "_DIALOG_ENTERED_":
        exists = False
        a = nameCurrent
        d = dialogueCurrentLine
        if not (a == d == ""):
            for actor in actors:
                if actor.get_name() == a:
                    exists = True
                    a = actor
                    break
            if not exists:
                a = Actor(a)
                actors.append(a)
            aindex = actors.index(a)

            actors[aindex].add_dialogue(d, tempindex)

            resetInputBoxes("","")
            updateNames()
            updateScript(tempindex)
            fixActorList(tempindex, actors[aindex])
            nameCurrent = ""
            dialogueCurrentLine = ""

            if tempindex == index:
                index+=1
                tempindex=index
            else:
                tempindex=index

    if event == "PJSON":
        print_to_json()

window.close()
