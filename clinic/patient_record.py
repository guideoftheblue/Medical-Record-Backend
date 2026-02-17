from clinic.note import Note
from .dao.note_dao_pickle import NoteDAOPickle

class PatientRecord:
    """Handles creation, retrieval, updating, and deletion of patient's notes.

       Attributes:
        phn (int): the personal health number (PHN) of the associated patient, used to initialize patient record
        file in note_dao
        autosave (bool): used to determine whether persistence is being used and tested, False unless assigned
        note_dao(NoteDAOPickle): DAO used to control the associated patient's notes

    """
    def __init__(self, phn, autosave = False)-> None:
        """Handles creation, retrieval, updating, and deletion of patient's notes.

        Attributes:
            phn (int): the personal health number (PHN) of the associated patient, used to initialize patient record
            file in note_dao
            autosave (bool): used to determine whether persistence is being used and tested, False unless assigned

        """
        self.phn = phn
        self.autosave = autosave
        self.note_dao = NoteDAOPickle(phn, autosave)


    def __str__(self)-> str: #DO LATER#
        """Returns a string representation of the PatientRecord for user purposes

        Returns:
            str: string representation of the Patient

        Example format::
            "Patient Record with 4 notes"
        """
        return "Patient Record with {} notes".format(len(self.note_dao.list_notes()))

    def __repr__(self)-> str: #DO LATER#
        """Provides in depth string representation of the PatientRecord for debugging purposes

        Returns:
            str: string representation of the PatientRecord

        Example format:
            "PatientRecord(autocounter, notes)"
        """
        return "PatientRecord({},{})".format(self.note_dao, self.notes)


    def __eq__(self, other)-> bool:
        """Checks if two PatientRecord instances are equal based on their list of notes.

        Args:
            other (PatientRecord): Another Patient instance to compare.

        Returns:
             bool: True if both instances have the same PHN, False otherwise.
        """
        return self.notes == other.notes

    def create_note(self, text:str)-> Note:
        """Creates a new note, assigns it a unique ID, and stores it in the notes dictionary.

        Args:
            text (str): The content of the new note.

        Returns:
            Note: The newly created note object.
        """

        return self.note_dao.create_note(text)

    def search_note(self, note_code:int)-> Note or None:
        """Searches for a note by its unique code in the dictionary of notes.

        Args:
            note_code (int): The id code of the note to search for.

        Returns:
            Note: The desired Note object if found
            None: if note not found
        """

        return self.note_dao.search_note(note_code)

    def retrieve_notes(self, search:str)->[Note]:
        """Finds notes that contains the specified search term

        Args:
            search(str): The string to search for.

        Returns:
            list of Note: The list of Notes with the search term in their text
        """
        return self.note_dao.retrieve_notes(search)

    def update_note(self, note_code:int, text:str)-> bool:
        """Updates the text of the desired note

            Args:
                note_code(int): ID code for the node to update.
                text(str): Updated text for desired note

            Returns:
                bool: True if desired note found
                      False if note not found
        """
        return self.note_dao.update_note(note_code, text)

    def delete_note(self, note_code:str)-> bool:
        """Deletes the desired note

            Args:
                note_code(int): ID code for the node to delete.

            Returns:
                bool: True if desired note found
                      False if note not found
        """
        return self.note_dao.delete_note(note_code)

    def list_notes(self)-> [Note]:
        """Returns a list of all the current patient's notes from newest to oldest

            Returns:
                list of Note: The current patient's notes from newest to oldest
        """
        return self.note_dao.list_notes()


