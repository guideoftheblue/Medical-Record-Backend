from clinic.patient_record import PatientRecord

class Patient:
    """Represents a patient in the system.

        Attributes:
            phn (str): The patient's personal health number (PHN)
            name (str): The patient's name
            birth_date(str): The patient's date of birth
            phone(str): The patient's phone number
            email(str): The patient's email
            address(str): The patient's address
            record(PatientRecord): The PatientRecord with this patient's notes, initialized by constructor
    """

    def __init__(self, phn:int, name:str, birth_date:str, phone:str, email:str, address:str, autosave = False)-> None:
        """Initializes a Patient with a Personal Health Number, name, date of birth, phone, email, address, and a
           PatientRecord to hold notes for the patient.

        Args:
            phn (int): The patient's personal health number (PHN)
            name (str): The patient's name
            birth_date(str): The patient's date of birth
            phone(str): The patient's phone number
            email(str): The patient's email
            address(str): The patient's address
            autosave (bool): used to determine whether persistence is being used and tested, False unless assigned
        """
        self.phn = phn
        self.name = name
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.address = address
        self.record = PatientRecord(phn, autosave)
        self.autosave = autosave


    def __str__(self)-> str:
        """Returns a string representation of the Patient for user purposes

        Returns:
            str: string representation of the Patient

        Example format::
            "Patient: Mike, PHN: 4354764, Phone: 1234567890, Email Address: emailemail@email.com"
        """
        return "Patient: {}, PHN: {}, Phone: {}, Email Address: {}".format(self.name, self.phn, self.phone, self.email)

    def __repr__(self)-> str:
        """Provides in depth string representation of the Patient for debugging purposes

        Returns:
            str: string representation of the Patient

        Example format:
            "Patient(phn, "name", "birth_date", "phone", "email", "address")"
        """
        return "Patient({}, \"{}\", \"{}\", \"{}\", \"{}\", \"{}\")".format(self.phn, self.name, self.birth_date, self.phone, self.email, self.address)


    def __eq__(self, other)-> bool:
        """Checks if two Patient instances are equal based on PHN.

        Args:
            other (Patient): Another Patient instance to compare.

        Returns:
            bool: True if both instances have the same PHN, False otherwise.
        """
        return (self.phn == other.phn and self.name == other.name and self.birth_date == other.birth_date
            and self.phone == other.phone and self.email == other.email and self.address == other.address)


