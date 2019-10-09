import pygame
from pygame import midi
scales = {
	"A_minor": {
		"standard": [-2,0,3,5,7],
		"chord": ["M", "m", "M", "m", "m"],
		"shift": [-1, 2, 4, 6, 9],
		"base_note": 57
	}
}

class gh_midi_synth:
	def __init__(self, joystick_number, midi_port):
		pygame.init()
		midi.init()
		self.joystick = pygame.joystick.Joystick(joystick_number)
		self.joystick.init()
		self.midiOut = midi.Output(midi_port)

		#if forceful_shift is true, the octaver will "jump" the note instead of cutting it
		self.forceful_shift = True
		self.octave_shift = 0
		#star power button, shifts up either 1 or 2 semitones
		self.sharp_shift = False
		#note_mappings represent what note every button is currently mapped to
		self.note_mappings = [0] * 5
		self.active_scale = scales["A_minor"]

		self.play_chords = True
		self.chord_mode = False
		self.active_scale = None

	@staticmethod
	def unconfuse(button):
		#buttons 2 and 3 are switched?
		if button == 3:
			return 2
		if button == 2:
			return 3
		return button

	def calc_note(self, button):
		return (self.active_scale["base_note"] + 
				(self.active_scale["standard"] if not self.sharp_shift else self.active_scale["shift"])[button] +
				12 * self.octave_shift)


	def play_note(self, button):
		button = self.unconfuse(button)
		#if there is somehow already a note being played by this, release it
		if self.note_mappings[button] != 0:
			self.release_note(button)
		#calculate note
		note =  (self.active_scale['base_note'] + 
				(self.active_scale["standard"] if not self.sharp_shift else self.active_scale["shift"])[button] +
				12 * self.octave_shift)
		#re-save this button's note mapping
		self.note_mappings[button] = note
		self.midiOut.note_on(note, 100)

	def release_note(self, button, silent=False):
		button = self.unconfuse(button)
		#if there is nothing being played
		note = self.note_mappings[button]
		if note == 0:
			if not silent:
				print("unable to release button")
			return
		self.midiOut.note_off(note)
		self.note_mappings[button] = 0

	def release_all_notes(self):
		for i in range(5):
			self.release_note(i, silent=True)

	def refresh_notes(self):
		for i in range(5):
			if self.note_mappings[self.unconfuse(i)] != 0:
				self.release_note(i, silent=True)
				self.play_note(i)

	def get_highest_note(self):
		for i in reversed(range(5)):
			if self.note_mappings[self.unconfuse(i)] != 0:
				return self.unconfuse(i)
		return None

	def pitch_bend(self, value):
		self.midiOut.pitch_bend(value)

	@staticmethod
	def minor_chord(root_note):
		return [root_note,
				root_note + 3,
				root_note + 7,
				root_note + 12]

	@staticmethod
	def major_chord(root_note):
		return [root_note,
				root_note + 4,
				root_note + 7,
				root_note + 12]

	@staticmethod
	def dom7_chord(root_note):
		return [root_note,
				root_note + 4,
				root_note + 7,
				root_note + 10]

	@staticmethod
	def min7_chord(root_note):
		return [root_note,
				root_note + 3,
				root_note + 7,
				root_note + 10]

	@staticmethod
	def maj7_chord(root_note):
		return [root_note,
				root_note + 4,
				root_note + 7,
				root_note + 11]

	def play_chord(self, button, invert=False, alter=False):
		self.release_all_notes()
		note = self.calc_note(button)
		chord = self.active_scale["chord"][note]
		self.active_chord_button = button
		if invert:
			chord = "M" if chord == "m" else "m"
		if alter:
			chord = "min7" if chord == "m" else "dom7"

		if chord == "M":
			chord_mappings = self.major_chord(note)
		if chord == "m":
			chord_mappings = self.minor_chord(note)
		if chord == "dom7":
			chord_mappings = self.dom7_chord(note)
		if chord == "min7":
			chord_mappings = self.min7_chord(note)
		for i in range(len(chord_mappings)):
			self.note_mappings[i] = chord_mappings[i]
		self.refresh_notes()

	def refresh_chord(self):
		self.play_chord(self.active_chord_button)
	
	def release_chord(self):
		self.active_chord_button = None
		self.release_all_notes()

	def run(self):
		while True:
			for event in pygame.event.get():
				#print(event, event.type)
				
				#process strummer position (octave shift)
				if event.type == pygame.JOYHATMOTION:
					if event.value[0] == 0:
						self.octave_shift = event.value[1]
						if self.forceful_shift:
							self.refresh_notes()
						if self.play_chords and self.octave_shift == -1:
							self.octave_shift = 0
							self.chord_mode = True
							self.release_all_notes()
				#button pressed
				if event.type == pygame.JOYBUTTONDOWN:
					#if the star power button was pressed
					if event.button == 6:
						self.sharp_shift = True
						if self.forceful_shift:
							self.refresh_notes()
					#if a note button was pressed
					if event.button in range(5):
						if self.chord_mode:
							self.play_chord(event.button)
						else:
							self.play_note(event.button)

				if event.type == pygame.JOYBUTTONUP:
					#if the star power button was released
					if event.button == 6:
						self.sharp_shift = False
						if self.forceful_shift:
							if self.chord_mode():
								self.refresh_chord()
							else:
								self.refresh_notes()

					#if a note button was released
					if event.button in range(5):
						if self.chord_mode:
							self.release_chord()
						else:
							self.release_note(event.button)

				#tilt or whammy
				if event.type == pygame.JOYAXISMOTION:
					if event.axis == 3 and not self.chord_mode:
						self.pitch_bend(int((event.value + 1)*1650))


if __name__ is "__main__":
	controller = gh_midi_synth(0,18)
	controller.run()
	midi.quit()