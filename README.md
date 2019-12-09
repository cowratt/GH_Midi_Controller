# Guitar Hero Midi Controller
This package turns an xbox 360 guitar hero controller into a full-blown midi controller complete with chords, pitch-bending, and all sorts of groovy things!

![Controls](/controls.jpg)

### WARNING: I am not a music theory expert. Please forgive any theory errors.

## Getting started
 * `pip install pygame==2.0.0.dev6` (or newer)
 * Connect your guitar hero controller to your pc via a wireless adapter
 * install loopMidi and create a virtual port.
 * `python main.py`

The software looks for a controller on port 0, and a midi connection on port 3, but both of these can be set in main.py.

## Playing Notes:
By default, the face buttons correspond to the notes in the Pentatonic scale with the minor root being on the 2nd note (Red), and the major root being on the third note(yellow). The strum bar can be used to shift +/- 1 octave. The large wide star power button can be used to shift any given note up to the next "inbetween" note in the scale. For example, it would shift the minor 1 to a minor 2. In cases where there are no actual scale notes between two notes, such as between blue, the minor 4th, and orange, the minor 5th, it just plays the note halfway between, which in this example would be the "blues note".


## Playing Chords:
pressing on pad will play a chord, where the root note cooresponds with the button you pressed. Whether the given chord is major/minor/other is preprogrammed and can be changed easily in `midi_notes.py`. Pressing the small circular pause button will convert a chord to its respective 7 chord. It turns minor chords to min7, major chords to maj7, and the major 5th note (green) to a dom7, because it is mixolydian. Wow, look at that attention to detail!

## Pitch bending:
The whammy bar bends notes up by 1 full note, though every midi software actually has a different amount that it bends. Again, your mileage may vary. This can be set at the top of midi_notes.py.


with a little bit of luck and practice, it is possible to play all 12 notes in the ocave with this setup. You may, however, need to press the star power button and hold the whammy bar down at the time time to get the flat minor 2nd and the sharp minor 6th.

Good luck!
