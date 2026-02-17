from unittest import TestCase
from unittest import main
from clinic.note import Note

class NoteTests(TestCase):

    def test_equality(self):
        note1 = Note(1, "Patient reports severe headache.")
        note1a = Note(1, "Patient reports severe headache.")
        note2 = Note(1, "Patient reports minor abdominal pain.")
        note3 = Note(2, "Patient reports minor abdominal pain.")

        self.assertIsNotNone(note1, "initializing note 1")
        self.assertEqual(note1, note1a, "same notes")
        self.assertNotEqual(note1, note2, "different notes")
        self.assertNotEqual(note2, note3, "different notes")

    def test_repr(self):
        note1 = Note(1, "Patient reports severe headache.")
        note1a = Note(1, "Patient reports severe headache.")
        note2 = Note(2, "Patient reports minor abdominal pain.")
        note3 = Note(3, "Patient reports major abdominal pain.")

        self.assertIsNotNone(repr(note1))

        self.assertEqual("Note(1, \"Patient reports severe headache.\")",
                         repr(note1), "Note 1 representation")
        self.assertEqual("Note(3, \"Patient reports major abdominal pain.\")",
                         repr(note3), "Note 3 representation")
        self.assertEqual(repr(note1a), repr(note1), "same notes, same representations")

        self.assertNotEqual(repr(note2), repr(note1), "different notes, different representations")
        self.assertNotEqual(repr(note3), repr(note1), "different notes, different representations")

    def test_str(self):
        note1 = Note(1, "Patient reports severe headache.")
        note1a = Note(1, "Patient reports severe headache.")
        note2 = Note(2, "Patient reports minor abdominal pain.")
        note3 = Note(3, "Patient reports major abdominal pain.")

        self.assertIsNotNone(str(note1))

        self.assertEqual("Note 1: Patient reports severe headache.",
                         str(note1), "Note 1 string")
        self.assertEqual("Note 3: Patient reports major abdominal pain.",
                         str(note3), "Note 3 string")
        self.assertEqual(str(note1a), str(note1), "same notes, same strings")

        self.assertNotEqual(str(note2), str(note1), "different notes, different strings")
        self.assertNotEqual(str(note3), str(note1), "different notes, different strings")


if __name__ == '__main__':
    unittest.main()