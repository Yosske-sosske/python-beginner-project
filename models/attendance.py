class Attendance:
    def __init__(self, date, time, employee_id, name):
        self.date = date
        self.time = time
        self.employee_id = employee_id
        self.name = name

    def __repr__(self):
        return f'The employee {self.name}, with the id: {self.employee_id}, marked attendance on {self.date} at {self.time}.'
