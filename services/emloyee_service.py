import csv
import pandas as pd
from csv import DictWriter
from end_project.models.employee import Employee


def check_row(employee_row):
    if len(employee_row) != 4:
        return False

    for index, item in enumerate(employee_row):
        if len(item) == 0:
            return False

        if (index == 1 and item.isdigit()) or (index != 1 and not item.isdigit()):
            return False

    return True


class EmployeeService:
    def __init__(self, file_name: str):
        self.file_name = file_name

    def get_employee(self, uid):
        with open(self.file_name, "r") as file:
            csvreader = csv.reader(file)

            next(csvreader)

            for row in csvreader:
                employee = Employee(*row)

                if employee.uid == str(uid):
                    return employee

            raise Exception(f"Employee with id: {uid} not found.")

    def add_employee(self, uid, name, phone, age):
        try:
            self.get_employee(uid)
            raise Exception(f"The employee with the id:{uid} already exists.")

        except Exception:
            pass

        new_row_to_add = [uid, name, phone, age]
        if not check_row(new_row_to_add):
            raise Exception(f"The data you entered is invalid")

        new_employee = {
            'id': uid,
            'name': name,
            'phone': phone,
            'age': age
        }

        with open(self.file_name, "a", newline="") as f_new_employee:
            dictwriter_object = DictWriter(f_new_employee, fieldnames=Employee.FIELD_NAMES)
            dictwriter_object.writerow(new_employee)

    def add_employees_from_file(self, employee_file_name):
        with open(employee_file_name, 'r') as new_file:
            csvreader = csv.reader(new_file)

            next(csvreader)

            valid_rows = []

            for index, row in enumerate(csvreader):
                if not check_row(row):
                    raise Exception(f"row number {index + 2},in {employee_file_name} is invalid.")

                valid_rows.append(row)

        for good_row in valid_rows:
            self.add_employee(*good_row)

    def delete_employee(self, uid):
        self.get_employee(uid)

        employee_df = pd.read_csv(self.file_name, index_col='id')
        employee_df = employee_df.drop(int(uid))
        employee_df.to_csv(self.file_name)

    def delete_employee_from_file(self, delete_employee_file_name):
        with open(delete_employee_file_name, 'r') as new_file:
            csvreader = csv.reader(new_file)

            next(csvreader)

            valid_ids = []

            for index, row in enumerate(csvreader):
                if len(row) != 1:
                    raise Exception(f"row number {index + 2} is empty")

                valid_uid = row[0]

                try:
                    self.get_employee(valid_uid)
                except Exception:
                    raise Exception(
                        f"The employee with the id: {valid_uid}, in row number {index + 2}, in "
                        f"{delete_employee_file_name} does not exist.")

                valid_ids.append(valid_uid)

        for uid in valid_ids:
            self.delete_employee(uid)
