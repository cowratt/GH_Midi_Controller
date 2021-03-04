from gh_controller import gh_controller
from midi_notes import noteController
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import midi, joystick



#helper functions to release and re-engage all notes, 
#used to refresh when changing things
def releaseAll():
    for i in GHController.activeNotes():
        MidiController.releaseNote(i)
    if GHController.pressed_pad != None:
        MidiController.releaseChord(GHController.pressed_pad)
def updateAll():
    for i in GHController.activeNotes():
        MidiController.playNote(i)
    if GHController.pressed_pad != None:
        MidiController.playChord(GHController.pressed_pad)


def notePressed(controllerButton):
    print("note pressed:", controllerButton)
    MidiController.playNote(controllerButton)

def noteReleased(controllerButton):
    print("note released:", controllerButton)
    MidiController.releaseNote(controllerButton)

def chordPressed(controllerButton):
    print("chord pressed:", controllerButton)
    MidiController.playChord(controllerButton)

def chordReleased(controllerButton):
    print("chord released:", controllerButton)
    MidiController.releaseChord(controllerButton)

def buttonPressed(controllerButton):
    print("ButtonPressed:", controllerButton)
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

def transpose(transposeValue):
	print("transpose:", transposeValue)
	MidiController.transpose(transposeValue)

def strumChanged(controllerButton):
    print("strum:", controllerButton)
    #forceful octave shift: release notes add shift, bring notes back
    releaseAll()
    MidiController.octaveShift = controllerButton
    updateAll()

if __name__ == "__main__":
	midi.init()
	print("Conrad Menchine's GH Midi Interface.\n",
		  "Available devices:")

	for i in range(midi.get_count()):
		info = midi.get_device_info(i)
		if(info[3]):
			print(str(i) + ": " + info[1].decode())

	read_input = True
	print("Which Midi output do you want to use? (Enter a number)")
	while read_input:
		try:
			MIDI_PORT_NUMBER = int(input("> "))
			read_input = False
		except:
			print("Invalid input. Please enter a number.")



	CONTROLLER_NUMBER = 0
	print("Using Controller", CONTROLLER_NUMBER)
	joystick.init()
	num_connected_controllers = joystick.get_count()
	if num_connected_controllers == 0:
		raise Exception("No Controllers found. Please Connect a controller and restart this program.")
	elif num_connected_controllers == 1:
		print("One controller found. Using it.")
	else:
		print("There are", joystick.get_count(), "controllers connected:")
		for i in range(num_connected_controllers):
			print(i + ": " + joystick.Joystick(i).get_name())



	GHController = gh_controller(CONTROLLER_NUMBER)
	MidiController = noteController(MIDI_PORT_NUMBER)
	#set up callbacks
	GHController.noteButtonPressedCallback = notePressed
	GHController.noteButtonReleasedCallback = noteReleased
	GHController.neckPadPressedCallback = chordPressed
	GHController.neckPadReleasedCallback = chordReleased
	GHController.otherButtonPressedCallback = buttonPressed
	GHController.otherButtonReleasedCallback = buttonReleased
	GHController.pitchBendCallback = pitchBend
	GHController.strumChangedCallback = strumChanged
	GHController.transposeCallback = transpose

	GHController.run()