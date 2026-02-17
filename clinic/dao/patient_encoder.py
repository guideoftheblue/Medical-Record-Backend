import json
from clinic.patient import Patient
class PatientEncoder(json.JSONEncoder): #based on SENG265 Python Persistence slides
    def default(self, obj):
        if isinstance(obj, Patient):
            return {"__type__": "Patient", "phn": obj.phn, "name": obj.name, "birth_date":obj.birth_date,
                    "phone":obj.phone,"email":obj.email, "address":obj.address}
        return super().default(obj)
