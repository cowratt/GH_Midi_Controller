from gh_controller import gh_controller
from midi_notes import noteController

GHController = gh_controller(0)
MidiController = noteController(3)

#helper functions to release and re-engage all notes, 
#used to refresh when changing things
def releaseAll():
    for i in GHController.activeNotes():
        MidiController.releaseNote(i)
def updateAll():
    for i in GHController.activeNotes():
        MidiController.playNote(i)


def notePressed(controllerButton):
    print("note pressed:", controllerButton)
    MidiController.playNote(controllerButton)

def noteReleased(controllerButton):
    print("note released:", controllerButton)
    MidiController.releaseNote(controllerButton)

def buttonPressed(controllerButton):
    print("button pressed:", controllerButton)
    releaseAll()
    if(controllerButton == 6): #star power button
        MidiController.noteShift = True
    if(controllerButton == 7): #start button
        MidiController.altered_chord = True
    updateAll()
def buttonReleased(controllerButton):
    print("button released:", controllerButton)
    releaseAll()
    if(controllerButton == 6): #star power button
        MidiController.noteShift = False
    if(controllerButton == 7): #start button
        MidiController.altered_chord = False
    updateAll()

def pitchBend(bendAmount):
    print("pitch:", bendAmount)
    MidiController.pitchBend(bendAmount)

def strumChanged(controllerButton):
    print("strum:", controllerButton)
    #forceful octave shift: release notes add shift, bring notes back
    releaseAll()
    MidiController.octaveShift = controllerButton
    updateAll()

GHController.noteButtonPressedCallback = notePressed
GHController.noteButtonReleasedCallback = noteReleased
GHController.otherButtonPressedCallback = buttonPressed
GHController.otherButtonReleasedCallback = buttonReleased
GHController.pitchBendCallback = pitchBend
GHController.strumChangedCallback = strumChanged

GHController.run()