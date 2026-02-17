import json
from clinic.patient import Patient
class PatientDecoder(json.JSONDecoder): #based on SENG265 Python Persistence slides
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        if '__type__' in dct and dct['__type__'] == 'Patient':
            return Patient(dct['phn'], dct['name'], dct['birth_date'], dct['phone'], dct['email'], dct['address'], True)
        return dct