from services.emloyee_service import EmployeeService
from services.attendance_service import AttendanceService


def main():
    has_position = False

    role_funcs = {
        "manager": handle_manager,
        "employee": handle_employee
    }

    while not has_position:
        position = input("Welcome! Are you a manager or an employee: ")

        if position != "manager" and position != "employee":
            print("You don't supposed to enter this system, please leave or I am calling the police.")

        else:
            has_position = True
            role_funcs[position]()


def handle_manager():
    global employee_service
    global attendance_service

    handle_m = True

    while handle_m:
        choice = input('''Please choose one of the following options:
1) add employee
2) add employees from another file
3) delete employee
4) delete employees from another file
5) employees attendance report
6) current month employees attendance report
7) late employees report       
8) exit the program 
''')

        try:
            match choice:
                case "1":
                    employee_id = input("Please enter employee's id: ")
                    employee_name = input("Please enter employee's name: ")
                    employee_phone = input("Please enter employee's phone number: ")
                    employee_age = input("Please enter employee's age: ")

                    employee_service.add_employee(employee_id, employee_name, employee_phone, employee_age)

                case "2":
                    new_employees_file = input("Please enter file path to add new employees: ")

                    employee_service.add_employees_from_file(new_employees_file)

                case "3":
                    delete_employee_id = input("Please enter the id of the unwanted employee: ")

                    employee_service.delete_employee(delete_employee_id)

                case "4":
                    delete_employee_file = input("Please enter file path to delete employees: ")

                    employee_service.delete_employee_from_file(delete_employee_file)

                case "5":
                    report_employee_id = input("Please enter employee's id you would like to get a report on: ")

                    attendance_service.attendance_report(report_employee_id)

                case "6":
                    attendance_service.current_month_report()

                case "7":
                    attendance_service.late_employees_report()

                case "8":
                    handle_m = False

                case _:
                    raise Exception("There is no such option, please try again.")

        except Exception as e:
            print(e)


def handle_employee():
    global attendance_service

    has_attendance = True

    while has_attendance:
        try:
            employee_attendance = input("Please enter your id to mark an attendance: ")
            attendance_service.mark_attendance(employee_attendance)

            print("Attendance was marked successfully")
            has_attendance = False

        except Exception as e:
            print(e)


if __name__ == '__main__':
    employee_service = EmployeeService("db/employee.csv")
    attendance_service = AttendanceService("db/attendance.csv", employee_service)

    main()
