class Employee:
    FIELD_NAMES = ['id', 'name', 'phone', 'age']

    def __init__(self, uid, name, phone, age):
        self.uid = uid
        self.name = name
        self.phone = phone
        self.age = age
