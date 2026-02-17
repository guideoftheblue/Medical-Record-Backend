from unittest import TestCase
from unittest import main
from clinic.patient import Patient
from clinic.note import Note
from clinic.patient_record import PatientRecord

class PatientRecordTests(TestCase):
    def test_create_search(self):
        patient = Patient(12345678, "Susan", "20040611", "7784539275",
                           "susanemail@email.com", "123 Susan Ave")
        record = patient.record
        note1 = Note(1, "Patient reports severe headache.")
        note1a = Note(1, "Patient reports severe headache.")
        note2 = Note(2, "Patient reports minor headache.")
        note3 = Note(3, "Patient reports minor backache.")

        #searching empty record
        self.assertIsNone(record.search_note(1), "empty notes")

        #Add note, code should be 1
        self.assertIsNotNone(record.create_note("Patient reports severe headache."),
                             "adding note 1 shouldn't fail")

        #Searching note that is in record, note that isn't in record
        self.assertIsNotNone(record.search_note(1), "searching note 1 shouldn't fail")
        self.assertIsNone(record.search_note(2), "searching note 2 should fail")
        self.assertEqual(record.search_note(1), note1a, "note 1a data should be same as note 1")

        # Add note, code should be 2
        self.assertIsNotNone(record.create_note("Patient reports minor headache."),
                             "adding note 2 shouldn't fail")
        # Add note, code should be 3
        self.assertIsNotNone(record.create_note("Patient reports minor backache."),
                             "adding note 3 shouldn't fail")

        self.assertEqual(note1, record.search_note(1), "note1 remains registered")
        self.assertEqual(note2, record.search_note(2), "note2 is registered")
        self.assertEqual(note3, record.search_note(3), "note3 is registered")

    def test_retrieve(self):
        patient = Patient(12345678, "Susan", "20040611", "7784539275",
                          "susanemail@email.com", "123 Susan Ave")
        record = patient.record

        note1 = Note(1, "Patient reports severe headache.")
        note2 = Note(2, "Patient reports minor headache.")
        note3 = Note(3, "Patient reports minor backache.")

        self.assertEqual(0, len(record.retrieve_notes("stomachache")), "empty record")

        record.create_note("Patient reports severe headache.")
        record.create_note("Patient reports minor headache.")
        record.create_note("Patient reports minor backache.")

        retrieved = record.retrieve_notes("backache")
        self.assertEqual(1, len(record.retrieve_notes("backache")),
                         "there should be 1 note containing 'backache'")
        self.assertEqual(note3, retrieved[0], "Retrieving backache note")

        retrieved = record.retrieve_notes("headache")
        self.assertEqual(2, len(record.retrieve_notes("headache")),
                         "there should be 2 notes containing 'headache'")
        self.assertEqual(note1, retrieved[0], "Retrieving severe headache note")
        self.assertEqual(note2, retrieved[1], "Retrieving minor headache note")


    def test_update(self):
        patient = Patient(12345678, "Susan", "20040611", "7784539275",
                          "susanemail@email.com", "123 Susan Ave")
        record = patient.record

        note1 = Note(1, "Patient reports severe headache.")
        note2 = Note(2, "Patient reports minor headache.")
        note3 = Note(3, "Patient reports minor backache.")

        self.assertFalse(record.update_note(1, "Patient reports severe stomachache"), "empty record")

        record.create_note("Patient reports severe headache.")
        record.create_note("Patient reports minor headache.")
        record.create_note("Patient reports minor backache.")

        self.assertFalse(record.update_note(4, "Patient reports severe nausea"), "Unadded note")

        self.assertTrue(record.update_note(1, "Patient reports severe stomachache"), "Updating Note 1, new text")
        self.assertTrue(record.update_note(2, "Patient reports severe headache"), "Updating Note 2, new text")

    def test_delete(self):
        patient = Patient(12345678, "Susan", "20040611", "7784539275",
                          "susanemail@email.com", "123 Susan Ave")
        record = patient.record

        note1 = Note(1, "Patient reports severe headache.")
        note2 = Note(2, "Patient reports minor headache.")
        note3 = Note(3, "Patient reports constant vomiting.")
        note4 = Note(4, "Patient reports severe right lower abdominal pain.")
        note5 = Note(5, "Patient reports loss of short term memory.")

        self.assertEqual(0, len(record.list_notes()), "empty record")

        record.create_note("Patient reports severe headache.")

        listed = record.list_notes()
        self.assertEqual(1, len(listed), "there should be 1 note in the list")
        self.assertEqual(note1, listed[0], "Listing Note 1")

        record.create_note("Patient reports minor headache.")
        record.create_note("Patient reports constant vomiting.")
        listed = record.list_notes()
        self.assertEqual(3, len(listed), "there should be 3 notes in the list")
        self.assertEqual(note3, listed[0], "Listing Note 3, notes should be listed in reverse order")
        self.assertEqual(note2, listed[1], "Listing Note 2")
        self.assertEqual(note1, listed[2], "Listing Note 1")

        record.delete_note(1)
        record.delete_note(3)
        listed = record.list_notes()
        self.assertEqual(1, len(listed), "there should be 1 note in the list")
        self.assertEqual(note2, listed[0], "Listing Note 2")

        record.create_note("Patient reports severe right lower abdominal pain.")
        record.create_note("Patient reports loss of short term memory.")
        listed = record.list_notes()
        self.assertEqual(3, len(listed), "there should be 3 notes in the list")
        self.assertEqual(note5, listed[0], "Listing Note 5")
        self.assertEqual(note4, listed[1], "Listing Note 4")
        self.assertEqual(note2, listed[2], "Listing Note 2")

        record.delete_note(2)
        record.delete_note(4)
        record.delete_note(5)
        self.assertEqual(0, len(record.list_notes()), "list should be empty")

    #def test_list(self):

