from pickle import load, dump
from .note_dao import NoteDAO
from clinic.note import Note

class NoteDAOPickle(NoteDAO):
    """DAO used to control the collection of this patient's notes

    Attributes:
    autocounter (int): tracker to determine the note code of the last created Note
    autosave (bool): used to determine whether persistence is being used and tested, False unless assigned
    notes (dict of int:Note): dict of current patients with {note code:Note}.
    phn (int): the personal health number (PHN) of the associated patient, used to initialize patient record file
    """

    def __init__(self, phn, autosave = False):
        """Initializes DAO for collection of patient Notes

        Args:
        phn (int): the personal health number (PHN) of the associated patient, used to initialize patient record file
        autosave (bool): used to determine whether persistence is being used and tested, False unless assigned
        """
        self.autocounter = 0
        self.autosave = autosave
        self.notes = {} #{note code:Note}
        self.phn = phn

        if self.autosave is True:
            self.load_patients()

    def load_patients(self):
        """Loads patient notes from dat file named (self.phn).dat into patient notes dictionary"""
        try:
            with open('clinic/records/{}.dat'.format(self.phn), 'rb') as file:
                self.notes = load(file)
                if self.notes:
                    self.autocounter = max(self.notes.keys())
        except FileNotFoundError: #if (self.phn).dat doesn't exist
            self.notes = {} #initialize dictionary as empty

    def save_patients(self):
        """Saves patient notes from patient notes dictionary into file named (self.phn).dat"""
        with open('clinic/records/{}.dat'.format(self.phn), 'wb') as file:
            dump(self.notes, file)

    def search_note(self, note_code)-> Note or None:
        """Searches for a note by its unique code in the dictionary of notes.

            Args:
                note_code (int): The id code of the note to search for.

            Returns:
                Note: The desired Note object if found
                None: if note not found
        """
        return self.notes.get(note_code)

    def create_note(self, text)-> Note:
        """Creates a new note, assigns it a unique ID, and stores it in the notes dictionary.

            Args:
                text (str): The content of the new note.

            Returns:
                Note: The newly created note object.
        """

        self.autocounter += 1
        new_note = Note(self.autocounter, text)
        self.notes[self.autocounter] = new_note
        if self.autosave is True:
            self.save_patients()
        return new_note

    def retrieve_notes(self, search)->[Note]:
        """Finds notes that contains the specified search term

            Args:
                search(str): The string to search for.

            Returns:
                list of Note: The list of Notes with the search term in their text
        """
        return [note for note in self.notes.values() if search in note.text]

    def update_note(self, note_code, text)-> bool:
        """Updates the text of the desired note

            Args:
                note_code(int): ID code for the node to update.
                text(str): Updated text for desired note

            Returns:
                bool: True if desired note found
                      False if note not found
        """
        if note_code not in self.notes:
            print("Note " + str(note_code) + " not found!")
            return False  # unable to update note

        self.notes[note_code].text = text

        if self.autosave is True:
            self.save_patients()
        return True

    def delete_note(self, note_code)-> bool:
        """Deletes the desired note

            Args:
                note_code(int): ID code for the node to delete.

            Returns:
                bool: True if desired note found
                      False if note not found
        """
        if note_code not in self.notes:
            print("Note " + str(note_code) + " not found!")
            return False  # unable to delete note

        del self.notes[note_code]

        if self.autosave is True:
            self.save_patients()
        return True

    def list_notes(self)-> [Note]:
        """Returns a list of all the current patient's notes from newest to oldest

            Returns:
                list of Note: The current patient's notes from newest to oldest
        """
        return [note for note in self.notes.values()][::-1]  #reverse list so most recent note comes first