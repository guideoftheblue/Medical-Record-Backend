import datetime
class Note:
    """Initializes a Note for a PatientRecord

    Args:
        code(int): The identifying code for this note
        text(str): the text contained in this note
        timestamp(datetime): the time this note was created, initialized by constructor
    """

    def __init__(self, code:int, text:str)-> None:
        """Initializes a Note for a PatientRecord

        Args:
            code(int): The identifying code for this note
            text(str): the text contained in this note
        """
        self.code = code
        self.text = text
        self.timestamp = datetime.datetime.now()

    def __str__(self)-> str:
        """Returns a string representation of the Note

        Returns:
            str: A string containing the text of the note

        Example Format:
            "Note 4: Patient reporting severe headache"
        """
        return "Note " + str(self.code) + ": " + self.text

    def __repr__(self):
        """Returns representation of the Note for debugging

        Returns:
            str: A string representing the Note object

        Example Format:
            "Note(code, "text")"
        """
        return "Note({}, \"{}\")".format(self.code, self.text)

    def __eq__(self, other)-> bool:
        """Checks if two Note instances are equal based on code and text.

        Args:
            other (Note): Another Note instance to compare.

        Returns:
            bool: True if both instances have the same code and text, False otherwise.
        """
        return self.code == other.code and self.text == other.text

    def update_info(self, text)-> None:
        """Updates a Note's text

        Args:
            text(str): The note's new text
        """
        self.text = text