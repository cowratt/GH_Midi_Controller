'''
This file contains the gh_controller class.
It provides easy callbacks for buttons on the guitar hero controller.
'''

import pygame
class gh_controller:
	#callbacks
	doNothing = lambda *args, **kwargs: None
	noteButtonPressedCallback = doNothing
	noteButtonReleasedCallback = doNothing

	neckPadPressedCallback = doNothing
	neckPadReleasedCallback = doNothing

	otherButtonPressedCallback = doNothing
	otherButtonReleasedCallback = doNothing
	
	pitchBendCallback = doNothing
	tiltNeckCallback = doNothing
	strumChangedCallback = doNothing

	pressed_buttons = [False] * 12
	pressed_pad = None

	def __init__(self, CONTROLLER_NUMBER):
		pygame.init()
		self.joystick = pygame.joystick.Joystick(CONTROLLER_NUMBER)
		self.joystick.init()
		self.CONTROLLER_NUMBER = CONTROLLER_NUMBER
		
	def activeNotes(self):
		#returns active notes
		return [i for i in range(5) if self.pressed_buttons[i]]
	
	def _updateNeckNote_(self, note):
		#helper function when updating which note is active on the touch pad
		if note == self.pressed_pad:
			return
		if self.pressed_pad != None:
			self.neckPadReleasedCallback(self.pressed_pad)
		self.pressed_pad = note
		if note != None:
			self.neckPadPressedCallback(note)

	def run(self):
		while True:
			for event in pygame.event.get():
				#process strummer position (octave shift)
				print(event)
				if event.type == pygame.JOYHATMOTION:
					if event.value[0] == 0:
						self.strumChangedCallback(event.value[1])
				#button pressed
				if event.type == pygame.JOYBUTTONDOWN:
					self.pressed_buttons[self.unconfuse(event.button)] = True
					#if a note button was pressed
					if event.button in range(5):
						self.noteButtonPressedCallback(self.unconfuse(event.button))
					#different button
					else:
						self.otherButtonPressedCallback(event.button)

				#button released
				if event.type == pygame.JOYBUTTONUP:
					self.pressed_buttons[self.unconfuse(event.button)] = False
					#if a note button was pressed
					if event.button in range(5):
						self.noteButtonReleasedCallback(self.unconfuse(event.button))
					#different button
					else:
						self.otherButtonReleasedCallback(event.button)

				#tilt or whammy
				if event.type == pygame.JOYAXISMOTION:
					if event.axis == 0:
						'''
						This means that the touchpad was moved. The touchpad sends its data via
						an analog slider. We 
						'''
						if event.value == 0.0:
							#pad was released
							self._updateNeckNote_(None)
						elif event.value <= -0.83:
							self._updateNeckNote_(0)
						elif event.value <= -0.40:
							self._updateNeckNote_(1)
						elif event.value <= 0.21:
							self._updateNeckNote_(2)
						elif event.value <= 0.58:
							self._updateNeckNote_(3)
						elif event.value <= 0.997:
							self._updateNeckNote_(4)
						else:
							print("invalid neckpad value:", event.value)
					if event.axis == 3:
						self.pitchBendCallback(event.value)
					if event.axis == 4:
						self.tiltNeckCallback(event.value)

				#print("pressed_buttons", self.pressed_buttons)
				#print("note mappings", self.button_mappings)
				#print(event, event.type)
				if event.type == 12:
					fail()
	@staticmethod
	def unconfuse(button):

		if button == 3:
			return 2
		if button == 2:
			return 3
		return button
