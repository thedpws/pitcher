from unittest import TestCase, skip, mock
import music as ptr


class TestNotes(TestCase):

    def test_init_sets_pitch_and_duration(self):
        # Arrange
        n = ptr.Note('C', 1.0)

        # Act
        pitch = n.pitch
        duration = n.duration

        # Assert
        self.assertEqual(pitch, 'C')
        self.assertEqual(duration, 1.0)

    def test_eq(self):
        # Arrange
        n1 = ptr.Note('C#', 1.0)
        n2 = ptr.Note('C#', 1.0)

        # Act
        equal = n1 == n2

        # Assert
        self.assertTrue(equal)

class TestRests(TestCase):
    
    def test_rest_init_sets_pitch_and_duration(self):
        # Arrange
        n = ptr.Rest(1.0)

        # Act
        pitch = n.pitch
        duration = n.duration

        # Assert
        self.assertEqual(pitch, None)
        self.assertEqual(duration, 1.0)

class TestMeasures(TestCase):

    def setUp(self):
        ptr.key(ptr.Key.C_MAJOR)
        ptr.time(ptr.Time.COMMON_TIME)

    def test_init_without_key_or_time_raises_exception(self):

        # Arrange
        ptr.key(None)
        ptr.time(None)

        # Act
        action = ptr.Measure

        # Assert
        self.assertRaises(Exception, action)
    
    def test_init_uses_global_key_and_time_signature(self):

        # Act
        m = ptr.Measure()

        # Assert
        self.assertEqual(m.key_signature, ptr.Key.C_MAJOR)
        self.assertEqual(m.time_signature, ptr.Time.COMMON_TIME)

    def test_extend_appends_all(self):

        # Arrange
        do = ptr.Note('C', 3/2)
        re = ptr.Note('D', 1/2)
        mi = ptr.Note('E', 3/2)

        notes = [do, re, mi]

        m = ptr.Measure()

        # Act
        m.extend(notes)

        # Assert
        self.assertEqual(m[0], do)
        self.assertEqual(m[1.5], re)
        self.assertEqual(m[2], mi)

    def test_append_appends(self):
        # Arrange
        ptr.key(ptr.Key.C_MAJOR)
        ptr.time(ptr.Time.COMMON_TIME)

        do = ptr.Note('C', 3/2)
        re = ptr.Note('D', 1/2)
        mi = ptr.Note('E', 3/2)

        m = ptr.Measure()

        # Act
        m.append(do)
        m.append(re)
        m.append(mi)

        # Assert
        self.assertEqual(m[0], do)
        self.assertEqual(m[1.5], re)
        self.assertEqual(m[2], mi)
