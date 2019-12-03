'''
This file contains the gh_controller class.
It provides easy callbacks for buttons on the guitar hero controller.
'''

import pygame
class gh_controller:
	#callbacks
	doNothing = lambda *args: None
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

	def __init__(self, CONTROLLER_NUMBER):
		pygame.init()
		self.joystick = pygame.joystick.Joystick(CONTROLLER_NUMBER)
		self.joystick.init()
		self.CONTROLLER_NUMBER = CONTROLLER_NUMBER
		
	def activeNotes(self):
		#returns active notes
		return [i for i in range(5) if self.pressed_buttons[i]]
	
	def run(self):
		while True:
			for event in pygame.event.get():
				#process strummer position (octave shift)
				#print(event)
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
					if event.axis == 3:
						self.pitchBendCallback(event.value)

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
