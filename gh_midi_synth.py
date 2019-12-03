import pygame
from pygame import midi
scales = {
	"A_minor": {
		"standard": [-2,0,3,5,7],
		"chord": ["M", "m", "M", "m", "m"],
		"shift": [-1, 2, 4, 6, 9],
		"base_note": 57,
		"octave_shift": -12,
	},
	"as_no_shame": {
		"standard": [-2,0,3,5,7],
		"octave": [-7, -5, -2, 2, 3],
		"chord": ["M", "m", "M", "m", "m"],
		"shift": [-1, 2, 4, 6, 9],
		"base_note": 57,
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
		#button_mappings represent what note every button is currently mapped to
		self.button_mappings = [0] * 5
		self.pressed_buttons = [False] * 5
		self.active_scale = scales["A_minor"]

		
		self.play_chords = True
		self.chord_mode = False
		#altered chord, alter me (m -> min7)
		self.altered_chord = False
		#altered chord, ALTER ME! (m -> M)
		self.alternate_chord = False

	@staticmethod
	def unconfuse(button):

		if button == 3:
			return 2
		if button == 2:
			return 3
		return button

	def calc_note(self, button):
		if "octave" in self.active_scale:
			return (self.active_scale["base_note"] + 
				(self.active_scale["standard"] if not self.octave_shift else self.active_scale["octave"])[button] + 
				(12 if self.octave_shift == 1 else 0))
		return (self.active_scale["base_note"] + 
				(self.active_scale["standard"] if not self.sharp_shift else self.active_scale["shift"])[button] +
				12 * self.octave_shift)


	def play_note(self, button):
		button = self.unconfuse(button)
		#if there is somehow already a note being played by this, release it
		if self.button_mappings[button] != 0:
			self.release_note(button)
		#calculate note
		note =  self.calc_note(button)
		#re-save this button's note mapping
		self.button_mappings[button] = note
		self.midiOut.note_on(note, 100)

	def release_note(self, button, silent=False):
		button = self.unconfuse(button)
		#if there is nothing being played
		note = self.button_mappings[button]
		if note == 0:
			if not silent:
				print("unable to release button")
			return
		self.midiOut.note_off(note)
		self.button_mappings[button] = 0

	def release_all_notes(self):

		for i in range(5):
			self.release_note(i, silent=True)

	def refresh_notes(self):

		for i in range(5):
			if self.button_mappings[self.unconfuse(i)] != 0:
				self.release_note(i, silent=True)
			if self.pressed_buttons[self.unconfuse(i)]:
				self.play_note(i)

	def get_highest_note(self):

		for i in reversed(range(5)):
			if self.pressed_buttons[i] != 0:
				return i
		return None

	def pitch_bend(self, value):
		#takes a value between 1 and -1
		v = int((value + 1)*1650)
		self.midiOut.pitch_bend(v)

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

	def play_chord(self, button):
		if self.get_highest_note() != self.unconfuse(button):
			return
		self.release_all_notes()
		button = self.unconfuse(button)
		chord = self.active_scale["chord"][button]
		note = self.calc_note(button) - 12

		print(note, chord)

		if self.alternate_chord:
			chord = "M" if chord == "m" else "m"
		if self.altered_chord:
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
			self.button_mappings[i] = chord_mappings[i]
			self.midiOut.note_on(chord_mappings[i], 100)
		print(self.button_mappings)

	def refresh_chord(self):
		if self.chord_mode:
			highest = self.get_highest_note()
			if highest is not None:
				self.play_chord(self.unconfuse(self.get_highest_note()))
			else:
				self.release_all_notes()
		else:
			self.refresh_notes()


	def run(self):
		while True:
			for event in pygame.event.get():
				#process strummer position (octave shift)
				print(event)
				if event.type == pygame.JOYHATMOTION:
					if event.value[0] == 0:
						self.octave_shift = event.value[1]
						if self.play_chords and self.octave_shift == -1:
							self.octave_shift = 0
							self.chord_mode = True
							self.release_all_notes()
						elif self.chord_mode:
							self.chord_mode = False
							self.refresh_chord()
						if self.forceful_shift:
							self.refresh_notes()
				#button pressed
				if event.type == pygame.JOYBUTTONDOWN:
					#if the start button was pressed
					if event.button == 7:
						self.alternate_chord = True
						self.refresh_chord()

					#if the star power button was pressed
					if event.button == 6:
						self.sharp_shift = True
						if self.forceful_shift:
							if self.chord_mode:
								self.refresh_chord()
							else:
								self.refresh_notes()

					#if a note button was pressed
					if event.button in range(5):
						self.pressed_buttons[self.unconfuse(event.button)] = True
						if self.chord_mode:
							self.play_chord(event.button)
						else:
							self.play_note(event.button)

				if event.type == pygame.JOYBUTTONUP:
					#if the start button was released
					if event.button == 7:
						self.alternate_chord = False
						self.refresh_chord()

					#if the star power button was released
					if event.button == 6:
						self.sharp_shift = False
						if self.forceful_shift:
							if self.chord_mode:
								self.refresh_chord()
							else:
								self.refresh_notes()

					#if a note button was released
					if event.button in range(5):
						self.pressed_buttons[self.unconfuse(event.button)] = False
						if self.chord_mode:
							self.refresh_chord()
						else:
							self.release_note(event.button)

				#tilt or whammy
				if event.type == pygame.JOYAXISMOTION:
					if event.axis == 3:
						if not self.chord_mode:
							self.pitch_bend(event.value)
						print(event.value)
						if self.chord_mode:
							if event.value > 0 and not self.altered_chord:
								self.altered_chord = True
								self.refresh_chord()
							elif event.value < 0 and self.altered_chord:
								self.altered_chord = False
								self.refresh_chord()

				#print("pressed_buttons", self.pressed_buttons)
				#print("note mappings", self.button_mappings)
				#print(event, event.type)
				if event.type == 12:
					fail()
if __name__ == "__main__":
	controller = gh_midi_synth(0,5)
	controller.run()
	midi.quit()
