from unittest import TestCase, skip, mock
import pitchr.music as ptr
from pitchr import *

from unittest import TestCase


class TestGlobals(TestCase):
    def test_key_signature_sets_globally(self):
        # Arrange
        ptr.key(Key.C_MAJOR)

        # Act
        key = ptr._key_signature

        # Assert
        self.assertEqual(key, Key.C_MAJOR)

    def test_time_signature_sets_globally(self):
        # Arrange
        ptr.time(Time.COMMON_TIME)

        # Act
        time = ptr._time_signature

        # Assert
        self.assertEqual(time, Time.COMMON_TIME)


class TestNotes(TestCase):

    def test_C4_maps_to_0(self):
        # Arrange
        n = Note('C4', 1.0)

        # Act
        pitch_number = n.pitch_number

        # Assert
        self.assertEqual(pitch_number, 0)

    def test_C4_maps_to_0(self):
        # Arrange
        n = Note('C4', 1.0)

        # Act
        pitch_number = n.pitch_number

        # Assert
        self.assertEqual(pitch_number, 0)

    def test_init_sets_pitch_and_duration(self):
        # Arrange
        n = Note('C', 1.0)

        # Act
        pitch = n.pitch
        duration = n.duration

        # Assert
        self.assertEqual(pitch, 'C4')
        self.assertEqual(duration, 1.0)

    def test_eq(self):
        # Arrange
        n1 = Note('C#', 1.0)
        n2 = Note('C#', 1.0)

        # Act
        equal = n1 == n2

        # Assert
        self.assertTrue(equal)


class TestRests(TestCase):

    def test_rest_init_sets_pitch_and_duration(self):
        # Arrange
        n = Rest(1.0)

        # Act
        pitch = n.pitch
        duration = n.duration

        # Assert
        self.assertEqual(pitch, None)
        self.assertEqual(duration, 1.0)
