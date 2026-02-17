from unittest import TestCase
from unittest import main
from clinic.patient import Patient

class PatientTests(TestCase):
    def test_equality(self):
        patient1 = Patient(12345678, "Susan", "20040611", "7784539275",
                           "susanemail@email.com", "123 Susan Ave")
        patient1a = Patient(12345678, "Susan", "20040611", "7784539275",
                            "susanemail@email.com", "123 Susan Ave")
        patient2 = Patient(90134567, "Mark", "20001111", "4039698427",
                           "markemail@email.com", "789 Mark Crescent")
        patient3 = Patient(73067358, "Tom", "19670829", "2503568842",
                           "tomemail@email.com", "456 Tom Street")

        self.assertIsNotNone(patient1, "initializing patient 1")
        self.assertEqual(patient1, patient1a, "same patients")
        self.assertNotEqual(patient1, patient2, "different patients")
        self.assertNotEqual(patient2, patient3, "different patients")

    def test_repr(self):
        patient1 = Patient(12345678, "Susan", "20040611", "7784539275",
                                "susanemail@email.com", "123 Susan Ave")
        patient1a = Patient(12345678, "Susan", "20040611", "7784539275",
                                 "susanemail@email.com", "123 Susan Ave")
        patient2 = Patient(90134567, "Mark", "20001111", "4039698427",
                                "markemail@email.com", "789 Mark Crescent")
        patient3 = Patient(73067358, "Tom", "19670829", "2503568842",
                                "tomemail@email.com", "456 Tom Street")

        self.assertIsNotNone(repr(patient1))

        self.assertEqual("Patient(12345678, \"Susan\", \"20040611\", \"7784539275\", \"susanemail@email.com\","
                         " \"123 Susan Ave\")",
                         repr(patient1), "Susan representation")
        self.assertEqual("Patient(73067358, \"Tom\", \"19670829\", \"2503568842\", \"tomemail@email.com\","
                         " \"456 Tom Street\")",
                         repr(patient3), "Tom representation")
        self.assertEqual(repr(patient1a), repr(patient1),"same patients, same representations")

        self.assertNotEqual(repr(patient2), repr(patient1),"different patients, different representations")
        self.assertNotEqual(repr(patient3), repr(patient1),"different patients, different representations")

    def test_str(self):
        patient1 = Patient(12345678, "Susan", "20040611", "7784539275",
                           "susanemail@email.com", "123 Susan Ave")
        patient1a = Patient(12345678, "Susan", "20040611", "7784539275",
                            "susanemail@email.com", "123 Susan Ave")
        patient2 = Patient(90134567, "Mark", "20001111", "4039698427",
                           "markemail@email.com", "789 Mark Crescent")
        patient3 = Patient(73067358, "Tom", "19670829", "2503568842",
                           "tomemail@email.com", "456 Tom Street")

        self.assertIsNotNone(str(patient1))

        self.assertEqual("Patient: Susan, PHN: 12345678, Phone: 7784539275, Email Address: susanemail@email.com",
                         str(patient1), "Susan string")
        self.assertEqual("Patient: Tom, PHN: 73067358, Phone: 2503568842, Email Address: tomemail@email.com",
                         str(patient3), "Tom string")
        self.assertEqual(str(patient1a), str(patient1), "same patients, same strings")

        self.assertNotEqual(str(patient2), str(patient1), "different patients, different strings")
        self.assertNotEqual(str(patient3), str(patient1), "different patients, different strings")
