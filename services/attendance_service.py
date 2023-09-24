import csv
import time
from csv import writer
from .emloyee_service import EmployeeService
from end_project.models.attendance import Attendance
from datetime import datetime, date, time as clock_time


class AttendanceService:
    TIME_FORMAT = "%H:%M:%S"
    DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, file_name: str, employee_service: EmployeeService):
        self.attendance_file = file_name
        self.employee_service = employee_service

    def mark_attendance(self, uid):
        current_employee = self.employee_service.get_employee(uid)

        employee_name = current_employee.name
        current_date = date.today()
        current_time = time.strftime(AttendanceService.TIME_FORMAT)

        attendance_attendance_row = [current_date, current_time, uid, employee_name]

        with open(self.attendance_file, 'a', newline='') as file:
            writer_object = writer(file)

            writer_object.writerow(attendance_attendance_row)

    def attendance_report(self, uid):
        self.employee_service.get_employee(uid)

        with open(self.attendance_file, 'r') as file:
            csvreader = csv.reader(file)

            next(csvreader)

            attendance_list = []

            for row in csvreader:
                attendance = Attendance(*row)

                if attendance.employee_id == str(uid):
                    attendance_list.append(attendance)

            print(f"Attendance report for the employee with the id:{uid}")

            for item in attendance_list:
                print(item)

    def current_month_report(self):
        current_month = datetime.now().month

        with open(self.attendance_file, 'r') as file:
            csvreader = csv.reader(file)

            next(csvreader)

            month_report_dict = {}

            for row in csvreader:
                attendance = Attendance(*row)

                current_date = datetime.strptime(attendance.date, AttendanceService.DATE_FORMAT)

                if current_date.month == current_month:
                    if attendance.name in month_report_dict:
                        month_report_dict[attendance.name] += 1
                    else:
                        month_report_dict[attendance.name] = 1

            print(f"Report for current month for all employees:")

            for key, value in month_report_dict.items():
                print(f"The employee {key}, marked attendance {value} times this month.")

    def late_employees_report(self):
        work_start_time = clock_time(9, 30)

        with open(self.attendance_file, 'r') as file:
            csvreader = csv.reader(file)

            next(csvreader)

            late_employees_report = {}

            for row in csvreader:
                attendance = Attendance(*row)

                arrival_time = datetime.strptime(attendance.time, AttendanceService.TIME_FORMAT).time()

                if arrival_time > work_start_time:
                    late_employees_report[attendance.name] = f"{attendance.time} on {attendance.date}"

            print(f"Report of all the employees who were late to work:")

            for name, arrival_date_time in late_employees_report.items():
                print(f"The employee {name}, arrived at {arrival_date_time}.")
