import hashlib
import os
from clinic.patient import Patient
from clinic.dao.patient_dao_json import PatientDAOJSON
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

class Controller:
    """A Controller to manage the clinic.

        Attributes:
        self.current_user(str): The current logged-in user. None if no user logged in.
        self.current_patient: The current patient set. None if no patient set.
        self.users(dict of str:str): Dict of current registered users with {username:password}.
        autosave (bool): used to determine whether persistence is being used and tested, False unless assigned
        patient_dao(PatientDAOJSON): DAO used to control the collection of patients
    """

    def __init__(self, autosave = False)-> None:
        """Initialize a Controller to manage clinic.

        Args:
        autosave (bool): used to determine whether persistence is being used and tested, False unless assigned
        """
        self.current_user = None
        self.current_patient = None
        self.users = {"user": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
                      "kala": "e5268ad137eec951a48a5e5da52558c7727aaa537c8b308b5e403e6b434e036e",
                      "ali": "6394ffec21517605c1b426d43e6fa7eb0cff606ded9c2956821c2c36bfee2810"}  # (username:password)
        self.autosave = autosave
        self.patient_dao = PatientDAOJSON(self.autosave)

        if autosave is True:
            self.users = {}
            current_dir = os.path.dirname(__file__)
            with open('clinic/users.txt', 'r') as file:
                for line in file:
                    user_log = line.split(',')
                    self.users[user_log[0].strip()] = user_log[1].strip()

    def get_password_hash(self, password): #taken from Lab 9 part A default code
        encoded_password = password.encode('utf-8')
        hash_object = hashlib.sha256(encoded_password)
        hex_dig = hash_object.hexdigest()
        return hex_dig

    def login(self, username:str, password:str)-> bool:
        """Attempts to log a user in with the provided username and password.

        Args:
            username (str): The username of the user attempting to log in.
            password (str): The password associated with the username.

        Returns:
            bool: True if login is successful

        Raises:
            DuplicateLoginException: if user is already logged in
            InvalidLoginException: if user doesn't exist or user:password combo is wrong

        Preconditions:
            self.current_user is None, meaning no user can be logged in to login.
        """
        if self.current_user is not None:
            raise DuplicateLoginException("User: " + self.current_user + " already logged in. Please log out first.")

        if username not in self.users:
            raise InvalidLoginException("User " + username + " does not exist.")

        password_hash = self.get_password_hash(password)
        if password_hash == self.users[username]:
            self.current_user = username
            return True

        raise InvalidLoginException("Incorrect username and/or password. Try again")

    def logout(self)-> bool:
        """Logs out the current user.

        Returns:
            bool: True if logout is successful; otherwise, False.

        Preconditions:
            self.current_user is not None, meaning a user must be a user logged in to logout.
        """
        if self.current_user is None:
            raise InvalidLogoutException("No user logged in!")

        self.current_user = None
        return True

    def create_patient(self, phn:int, name:str, birth_date:str, phone:str, email:str, address:str)-> Patient:
        """Creates a new patient, assigns it info, and stores it in the patient dictionary.

        Args:
            phn (str): The patient's personal health number (PHN).
            name (str): The patient's name.
            birth_date(str): The patient's date of birth.
            phone(str): The patient's phone number.
            email(str): The patient's email.
            address(str): The patient's address.

        Returns:
            Patient: the Patient object if successfully created

        Raises:
            IllegalAccessException: if no user is logged in
            IllegalOperationException: if a patient with that phn already exists in collection

        Preconditions:
            self.current_user is not None, meaning a user must be logged in to create for a patient.
            Patient with phn not already in system
        """

        if self.current_user is None: #if no user is logged in
            raise IllegalAccessException("No user logged in!")

        if self.search_patient(phn) is not None: #if patient already exists
            raise IllegalOperationException("System with that PHN already in system, cannot add patient.")

        new_patient = Patient(phn, name, birth_date, phone, email, address, self.autosave)
        return self.patient_dao.create_patient(new_patient)

    def search_patient(self, phn:int)-> Patient or None:
        """Searches for a patient by their Personal Health Number.

        Args:
            phn (int): The personal health number of the patient to search for.

        Returns:
            Patient: the Patient with phn if found
            None: if Patient with phn is not found

        Raises:
            IllegalAccessException: if no user is logged in

        Preconditions:
            self.current_user is not None, meaning a user must be logged in to search for a patient.
        """
        if self.current_user is None:
            raise IllegalAccessException("No user logged in!")

        return self.patient_dao.search_patient(phn)

    def retrieve_patients(self, name:str)-> [Patient]:
        """Retrieves a list of patients whose names contain the specified substring.

        Args:
            name (str): The substring to search for within patient names.

        Returns:
            list of Patient: A list of Patients with names containing name

        Raises:
            IllegalAccessException: if no user is logged in

        Preconditions:
            self.current_user is not None, meaning a user must be logged in to retrieve patients.
        """
        if self.current_user is None:
            raise IllegalAccessException("No user logged in!")

        return self.patient_dao.retrieve_patients(name)

    def update_patient(self, search_phn:int, phn:int, name:str, birth_date:str, phone:str, email:str, address:str)-> bool:
        """Updates a Patient's information based on their current phn.

        Args:
            search_phn: The patient's current personal health number (PHN)
            phn (str): The patient's new personal health number (PHN).
            name (str): The patient's new name.
            birth_date(str): The patient's new date of birth.
            phone(str): The patient's new phone number.
            email(str): The patient's new email.
            address(str): The patient's new address.

        Returns:
            bool: True if the update was successful; False otherwise.

        Raises:
            IllegalAccessException: if no user is logged in
            IllegalOperationException: if Patient with phn not in collection or if updated phn already in system
            or if the current Patient is being updated

        Preconditions:
            self.current_user is not None, meaning a user must be logged in to update a patient.
            search_phn must exist in self.patients.
            an updated phn cannot already be in collection
            current Patient is not being updated
        """
        if self.current_user is None:
            print("No user logged in!")
            raise IllegalAccessException("No user logged in!")

        if self.search_patient(search_phn) is None:
            raise IllegalOperationException("Patient with phn: " + str(search_phn) + " not found")

        if phn != search_phn and self.search_patient(phn) is not None:
            raise IllegalOperationException("Cannot update patient, new PHN already in system.")

        if self.current_patient is not None and phn == self.current_patient.phn:
            raise IllegalOperationException("Cannot update current patient! Unset patient first.")

        patient = Patient(phn, name, birth_date, phone, email, address)
        return self.patient_dao.update_patient(phn, patient)

    def delete_patient(self, phn:int)-> bool:
        """Deletes a patient from the records based on their Personal Health Number (PHN).

        Args:
            phn (int): The personal health number of the patient to be deleted.

        Returns:
            bool: True if the deletion was successful; False otherwise.

        Raise:
            IllegalAccessException: if no user is logged in
            IllegalOperationException: if Patient with phn is not in system or if the current Patient is being deleted

        Preconditions:
            self.current_user is not None, meaning a user must be logged in to update a patient.
            phn must exist in self.patients.
            current Patient cannot is not being deleted
        """
        if self.current_user is None:
            raise IllegalAccessException("No user logged in!")

        if self.search_patient(phn) is None:
            raise IllegalOperationException("Patient with phn: " + str(phn) + " not found")

        if self.current_patient is not None and phn == self.current_patient.phn:
            raise IllegalOperationException("Cannot delete current patient! Unset patient first.")

        return self.patient_dao.delete_patient(phn)

    def list_patients(self)-> [Patient]:
        """Lists all patients in the system.

        Returns:
            list of Patient: A list of all `Patient` objects

        Raises:
            IllegalAccessException: if no user is logged in

        Preconditions:
           self.current_user is not None, meaning a user must be logged in to update a patient.
        """
        if self.current_user is None:
            raise IllegalAccessException("No user logged in!")

        return self.patient_dao.list_patients()

    def set_current_patient(self, phn:int) -> None:
        """Sets the desired patient to the current patient.

        Args:
            phn: The desired patient's phn.

        Raises:
            IllegalAccessException: if no user is logged in
            IllegalOperationException: if Patient with phn is not in collection

        Preconditions:
           self.current_user is not None, meaning a user must be logged in to update a patient.
           Patient with phn is in patient collection
        """
        if self.current_user is None:
            raise IllegalAccessException("No user logged in!")

        elif self.search_patient(phn) is None:
            raise IllegalOperationException("Patient not found!")

        else:
            self.current_patient = self.search_patient(phn)

    def unset_current_patient(self)-> None:
        """
        Unsets the current patient.

        Raises:
            IllegalAccessException: if no user is logged in
            NoCurrentPatientException: if no Patient is selected

        Preconditions:
           self.current_user is not None, meaning a user must be logged in to update a patient.
           a Patient must be currently selected
        """
        if self.current_user is None:
            raise IllegalAccessException("No user logged in!")

        elif self.current_patient is None:
            raise NoCurrentPatientException("No patient selected!")

        else:
            self.current_patient = None

    def get_current_patient(self)-> Patient or None:
        """Returns the current patient.

        Returns:
            Patient: if a patient is selected
            None: if a patient is not selected

        Raises:
            IllegalAccessException: if no user is logged in

        Preconditions:
            self.current_patient is not None, meaning a patient must be selected.
        """
        if self.current_user is None:
            raise IllegalAccessException("No user logged in!")

        if self.current_patient is None:
            print ("No patient selected!")
            return None

        return self.current_patient

    def create_note(self, text:str):
        """Creates a new note, assigns it a unique ID, and stores it in the notes dictionary.

        Args:
            text (str): The content of the new note.

        Returns:
            Note: The newly created note object.

        Raises:
            IllegalAccessException: if no user is logged in
            NoCurrentPatientException: if no Patient is selected

        Preconditions:
            self.current_user is not None, meaning a user is logged in.
            self.current_patient is not None, meaning a patient is selected.
        """
        if self.current_user is None:
            raise IllegalAccessException("No user logged in!")

        if self.current_patient is None:
            raise NoCurrentPatientException("No patient selected!")

        return self.current_patient.record.create_note(text)

    def search_note(self, note_code:int):
        """Searches for a note by its unique code in the dictionary of notes.

        Args:
            note_code (int): The id code of the note to search for.

        Returns:
            Note: The desired Note object if found.
            None: if object is not found, no user is logged in or a patient is not selected.

        Raises:
            IllegalAccessException: if no user is logged in
            NoCurrentPatientException: if no Patient is selected

        Preconditions:
            self.current_user is not None, meaning a user is logged in.
            self.current_patient is not None, meaning a patient is selected.
        """
        if self.current_user is None:
            raise IllegalAccessException("No user logged in!")

        if self.current_patient is None:
            raise NoCurrentPatientException("No patient selected!")

        return self.current_patient.record.search_note(note_code)

    def retrieve_notes(self, search:str):
        """Finds notes in dict of notes that contains the specified search term.

        Args:
            search(str): The string to search for.

        Returns:
            list of Note: The list of Notes with the search term in their text.
            None: if no user is logged in or a patient is not selected.

        Raises:
            IllegalAccessException: if no user is logged in
            NoCurrentPatientException: if no Patient is selected

        Preconditions:
            self.current_user is not None, meaning a user is logged in.
            self.current_patient is not None, meaning a patient is selected.
        """
        if self.current_user is None:
            raise IllegalAccessException("No user logged in!")

        if self.current_patient is None:
            raise NoCurrentPatientException("No patient selected!")

        return self.current_patient.record.retrieve_notes(search)

    def update_note(self, note_code:int, text:str)-> bool:
        """Updates the text of the desired note.

        Args:
            note_code(int): ID code for the node to update.
            text(str): Updated text for note.

        Returns:
            bool: True if desired note is found and a user is logged in.
                  False if note is not found, no user is logged in or a patient is not selected.

        Raises:
            IllegalAccessException: if no user is logged in
            NoCurrentPatientException: if no Patient is selected

        Preconditions:
            self.current_user is not None, meaning a user is logged in.
            self.current_patient is not None, meaning a patient is selected.
        """
        if self.current_user is None:
            raise IllegalAccessException("No user logged in!")

        if self.current_patient is None:
            raise NoCurrentPatientException("No patient selected!")

        return self.current_patient.record.update_note(note_code, text)

    def delete_note(self, note_code:int)-> bool:
        """Deletes the desired note

        Args:
            note_code(int): ID code for the node to delete.

        Returns:
            bool: True if desired note found.
                  False if note is not found, no user is logged in, or a patient is not selected.

        Raises:
            IllegalAccessException: if no user is logged in
            NoCurrentPatientException: if no Patient is selected

        Preconditions:
            self.current_user is not None, meaning a user is logged in.
            self.current_patient is not None, meaning a patient is selected.
        """
        if self.current_user is None:
            raise IllegalAccessException("No user logged in!")

        if self.current_patient is None:
            raise NoCurrentPatientException("No patient selected!")

        return self.current_patient.record.delete_note(note_code)

    def list_notes(self):
        """Returns a list of all the current patient's notes

        Returns:
            list of Note: The current patient's notes.
            None: no user is logged in or patient is not selected.

        Raises:
            IllegalAccessException: if no user is logged in
            NoCurrentPatientException: if no Patient is selected

        Preconditions:
            self.current_user is not None, meaning a user is logged in.
            self.current_patient is not None, meaning a patient is selected.
        """
        if self.current_user is None:
            raise IllegalAccessException("No user logged in!")

        if self.current_patient is None:
            raise NoCurrentPatientException("No patient selected!")

        return self.current_patient.record.list_notes()
