import pygame
from pygame import midi
pygame.init()
midi.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

for i in range(pygame.midi.get_count()):
    print(i,pygame.midi.get_device_info(i))
midiOut = midi.Output(18)

forceful_octave_shift = True

octave_shift = 0
sharp_shift = False
base_note = 55

note_mappings = [0] * 5

scales = {
    "minor": {
        "standard": [-2,0,3,5,7],
        "shift": [-1, 2, 4, 6, 8],
    }
}

active_scale = scales["minor"]

def unconfuse(button):
    #buttons 2 and 3 are switched?
    if button == 3:
        return 2
    if button == 2:
        return 3
    return button

def play_note(button):
    button = unconfuse(button)
    #if there is somehow already a note being played by this, release it
    if note_mappings[button] != 0:
        release_note(button)
    #calculate note
    note =  (base_note + 
            (active_scale["standard"] if not sharp_shift else active_scale["shift"])[button] +
            12 * octave_shift)
    #re-save this button's note mapping
    note_mappings[button] = note
    midiOut.note_on(note, 100)

def release_note(button):
    button = unconfuse(button)
    #if there is nothing being played
    note = note_mappings[button]
    if note == 0:
        print("unable to release button")
        return
    midiOut.note_off(note)
    note_mappings[button] = 0

def refresh_notes():
	for i in range(5):
		if note_mappings[unconfuse(i)] != 0:
			release_note(i)
			play_note(i)

def get_highest_note():
	for i in reversed(range(5)):
		if note_mappings[unconfuse(i)] != 0:
			return unconfuse(i)
	return None

def pitch_bend(value):
	midiOut.pitch_bend(value)

while True:

    for event in pygame.event.get():
        #print(event, event.type)
        
        #process strummer position (octave shift)
        if event.type == pygame.JOYHATMOTION:
            if event.value[0] == 0:
                octave_shift = event.value[1]
                if forceful_octave_shift:
                	refresh_notes()

        #button pressed
        if event.type == pygame.JOYBUTTONDOWN:
            #if a note button was pressed
            if event.button in range(5):
                play_note(event.button)

            #if the star power button was pressed
            if event.button == 6:
                sharp_shift = True
                if not poly:
                	refresh_notes()

        if event.type == pygame.JOYBUTTONUP:
            #if a note button was released
            if event.button in range(5):
                release_note(event.button)

            #if the star power button was released
            if event.button == 6:
                sharp_shift = False
                if not poly:
                	refresh_notes()
        #tilt or whammy
        if event.type == pygame.JOYAXISMOTION:
        	if event.axis == 3 and not poly:
        		pitch_bend(int((event.value + 1)*1650))

                


midi.quit()
