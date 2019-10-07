import pygame
pygame.init()
pygame.midi.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

for i in range(pygame.midi.get_count):
    print(pygame.midi.get_device_info(i))

poly = False
forceful_octave_shift = False

octave_shift = 0
sharp_shift = False
base_note = 58

note_mappings = [0] * 5

scales = {
    "minor": {
        "standard": [-2,0,3,5,7],
        "shift": [-1, 2, 4, 6, 9],
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
    note =  base_note + 
            (active_scale["standard"] if not sharp_shift else active_scale["shift"])[button] +
            12 * octave_shift
    #re-save this button's note mapping
    note_mappings[button] = note
    pygame.midi.Output.note_on(note)

def release_note(button):
    button = unconfuse(button)
    #if there is nothing being played
    note = note_mappings[button]
    if note == 0:
        print("unable to release button")
        return
    pygame.midi.Output.note_off(note)
    note_mappings[button] = 0


while True:
    get input
    if keyChange:
        for event in pygame.event.get():
            print(event, event.type)
            
            #process strummer position (octave shift)
            if event.type == 9:
                if event.value[0] == 0:
                    octave_shift = event.value[1]

            #button pressed
            if event.type == 10:
                #if a note button was pressed
                if event.button in range(5):
                    play_note(event.button)

                #if the star power button was pressed
                if event.button == 6:
                    sharp_shift = True
            if keyReleased:
                process_input