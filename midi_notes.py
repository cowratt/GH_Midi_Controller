import pygame
from pygame import midi

PITCH_BEND_SCALE= 1650

'''
This file contains lots of vaugely generic midi controller code.
This can hopefully be used for all sorts of midi controllers.
The noteTranslater calculates the correct note given the state of the controls,
and the notePlayer plays or releases a given note, ignoring state
'''

#five note scale. Essentially a minor pentatonic where the root is the 2nd note.
#using the shifted notes, it's possible to play 10 out of the 12 notes:
# 0, 2, ,m3, M3, 4, 5b, 5, 6, m7, M7
#this leaves out the flat 2nd (phrygian) and the flat 6th, but its fine
scale =  {
	"standard": [-2,0,3,5,7],
	"chord": ["M", "m", "M", "m", "m"],
	"shift": [-1, 2, 4, 6, 8],
	"shiftChord": ["dom7", "m", "dom7", "maj7", "M"],
	"base_note": 57,
}



class noteTranslater:
	'''
	Contains methods to calculate the correct note,
	given that you're playing the nth note in a given scale.
	'''
	octaveShift = 0
	noteShift = False # play non-pentatonic notes
	altered_chord = False # m->min7
	base_note = 57
	def __init__(self):
		self.scale = scale
	def calcNote(self, noteNumber):
		scale = self.scale['standard'] if not self.noteShift else self.scale['shift']
		return scale[noteNumber] + 12*self.octaveShift + self.base_note

	def calcChord(self, noteNumber):
		scale = self.scale['chord'] if not self.noteShift else self.scale['shiftChord']
		chord = scale[noteNumber]
		note = self.calcNote(noteNumber) - 12
		if self.altered_chord:
			chord = "min7" if chord == "m" else "dom7"
		#calculate chord mappings
		if chord == "M":
			chord_mappings = self.major_chord(note)
		elif chord == "m":
			chord_mappings = self.minor_chord(note)
		elif chord == "dom7":
			chord_mappings = self.dom7_chord(note)
		elif chord == "min7":
			chord_mappings = self.min7_chord(note)
		elif chord == "maj7":
			chord_mappings = self.maj7_chord(note)
		else:
			print("ERROR WITH CHORD MAPPINGS")
		return chord_mappings


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



class notePlayer:
	def __init__(self, port):
		pygame.init()
		midi.init()
		self.midiOut = midi.Output(port)
	
	def noteOn(self, note, channel=0, velocity=100):
		print("note on:", note)
		self.midiOut.note_on(note, velocity, channel)
	def noteOff(self, note, channel=0, velocity=None):
		print("note off:", note)
		self.midiOut.note_off(note, channel=channel)
	def pitchBend(self, bend_amt):
		#takes a value between 1 and -1
		v = int((bend_amt + 1) * PITCH_BEND_SCALE)
		self.midiOut.pitch_bend(v)

class noteController(noteTranslater, notePlayer):
	def __init__(self, port):
		noteTranslater.__init__(self)
		notePlayer.__init__(self, port)
		pass
	def playNote(self, noteNumber):
		self.noteOn(self.calcNote(noteNumber), channel=0)
	def releaseNote(self, noteNumber):
		self.noteOff(self.calcNote(noteNumber), channel=0)
		
	def playChord(self, noteNumber):
		chord = self.calcChord(noteNumber)
		for note in chord:
			self.noteOn(note, channel=1)
		pass
	
	def releaseChord(self, noteNumber):
		chord = self.calcChord(noteNumber)
		for note in chord:
			self.noteOff(note, channel=1)
		pass