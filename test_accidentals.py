from pitchr import *

import unittest

class TestAccidentals(unittest.TestCase):

    def test_foreign_accidentals_play(self):

        # Should sound in Minor scale
        m = Measure([
            Note('C', 1.0),
            Note('D', 1.0),
            Note('Eb', 1.0),
            Note('F', 1.0),
            Note('G', 1.0),
            Note('Ab', 1.0),
            Note('Bb', 1.0),
            Note('C5', 1.0),
        ])

        m.play()

        self.assertEqual(input('Did you hear a minor key? [y/N]'), 'y')

    def test_native_accidentals_play(self):
        key(Key.Eb_MAJOR)
        m = Measure([
            Note('C', 1.0),
            Note('D', 1.0),
            Note('Eb', 1.0),
            Note('F', 1.0),
            Note('G', 1.0),
            Note('Ab', 1.0),
            Note('Bb', 1.0),
            Note('C5', 1.0),
        ])

        m.play()

        self.assertEqual(input('Did you hear a minor key? [y/N]'), 'y')

    def test_foreign_accidentals_show(self):

        m = Measure([
            Note('C', 1.0),
            Note('D', 1.0),
            Note('Eb', 1.0),
            Note('F', 1.0),
            Note('G', 1.0),
            Note('Ab', 1.0),
            Note('Bb', 1.0),
            Note('C5', 1.0),
        ])

        m.show()

        self.assertEqual(input('Did you see flats on Eb, Ab, Bb? [y/N]'), 'y')

    def test_native_accidentals_dont_show(self):


        key(Key.Eb_MAJOR)
        m = Measure([
            Note('C', 1.0),
            Note('D', 1.0),
            Note('Eb', 1.0),
            Note('F', 1.0),
            Note('G', 1.0),
            Note('Ab', 1.0),
            Note('Bb', 1.0),
            Note('C5', 1.0),
        ])

        m.show()

        self.assertEqual(input('Did you see no flats? [y/N]'), 'y')

    def test_key_signature_shows(self):


        key(Key.Eb_MAJOR)
        m = Measure([
            Note('C', 1.0),
            Note('D', 1.0),
            Note('Eb', 1.0),
            Note('F', 1.0),
            Note('G', 1.0),
            Note('Ab', 1.0),
            Note('Bb', 1.0),
            Note('C5', 1.0),
        ])

        m.show()

        self.assertEqual(input('Do you see 3 flats in the key signature? [y/N]'), 'y')
