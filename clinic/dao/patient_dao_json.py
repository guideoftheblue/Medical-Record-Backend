from .patient_dao import PatientDAO
from .patient_decoder import PatientDecoder
from .patient_encoder import PatientEncoder
from json import load, dump, JSONDecodeError


class PatientDAOJSON(PatientDAO):
    """DAO used to control the collection of patients

    Attributes:
    patients (dict of int:Patient): Dict of current patients with {phn:Patient}.
    autosave (bool): used to determine whether persistence is being used and tested, False unless assigned
    """

    def __init__(self, autosave = False):
        """Initializes DAO for collection of Patients

        Args:
        autosave (bool): used to determine whether persistence is being used and tested, False unless assigned
        """

        self.patients = {} #{phn:Patient}
        self.autosave = autosave

        if self.autosave is True:
            self.load_patients()

    def load_patients(self):
        """Loads patients from json file named patients.json into patient dictionary"""
        try:
            with open('clinic/patients.json', 'r') as file:
                data = load(file, cls=PatientDecoder)
                for patient in data: #load
                    self.patients[patient.phn] = patient #fill dictionary with patients in form {phn:Patient}
        except FileNotFoundError:
            file = open('clinic/patients.json', 'x') #create file if not yet created
            file.close()
        except JSONDecodeError: #if file is empty
            self.patients = {} #initialize patient collection to empty

    def save_patients(self):
        """Saves patients from patient dictionary into file named patients.json"""
        with open('clinic/patients.json', 'w') as file:
            dump(list(self.patients.values()), file, cls=PatientEncoder)

    def search_patient(self, phn):
        return self.patients.get(phn)

    def create_patient(self, patient):
        """Stores newly created patient in the patient collection.

        Args:
            patient (Patient): newly created patient

        Returns:
            Patient: the newly created Patient object
        """

        self.patients[patient.phn] = patient
        if self.autosave:
            self.save_patients()
        return patient


    def retrieve_patients(self, name):
        """Retrieves a list of patients whose names contain the specified substring.

        Args:
            name (str): The substring to search for within patient names.

        Returns:
            list of Patient: A list of Patients with names containing name
        """
        return [patient for patient in self.patients.values() if name.lower() in patient.name.lower()]

    def update_patient(self, phn, patient):
        """Updates a Patient's information based on their current phn.

            Returns:
            bool: True if the update was successful
        """
        if patient.phn != phn: #if new phn != old phn
            del self.patients[phn] #remove old phn from the collection

        self.patients[patient.phn] = patient
        if self.autosave:
            self.save_patients()

        return True

    def delete_patient(self, phn):
        """
        Deletes a patient from the records based on their Personal Health Number (PHN).

        Args:
            phn (int): The personal health number of the patient to be deleted.

        Returns:
            bool: True if the deletion was successful
        """
        del self.patients[phn]
        if self.autosave:
            self.save_patients()
        return True

    def list_patients(self):
        """Lists all patients in the system.

        Returns:
            list of Patient: A list of all `Patient` objects in collection
        """

        return [patient for patient in self.patients.values()]
