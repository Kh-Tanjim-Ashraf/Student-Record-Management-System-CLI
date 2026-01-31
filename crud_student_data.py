import os, csv, time

FILE_PATH = './students.csv'

CSV_HEADER = ['Name', 'Roll', 'Email', 'Department']

class CRUD_CSV:
    def __init__(self):
        pass
    
    def user_input(self) -> list:
        usr_name = input("Enter student name: ")
        usr_roll = input("Enter roll number: ")
        usr_email = input("Enter email address: ")
        usr_deprmnt = input("Enter department: ")
        return [usr_name, usr_roll, usr_email, usr_deprmnt]
        
    def add_student(self, data):
        with open(FILE_PATH, mode='a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            data = self.user_input()
            csv_writer.writerow(data)
            print("Student record added successfully!")


class LoadCSV:
    def __init__(self):
        if os.path.exists(FILE_PATH):
            print("Welcome to the Student Record Management System!")
        else:
            # Create a new file, but it will return an error if the file exist
            with open(FILE_PATH, 'x', newline='', encoding='utf-8') as new_csv:
                csv_file = csv.writer(new_csv)
                csv_file.writerow(CSV_HEADER)
            print("New student file created!")
        # Instantiate the student CRUD operation class
        self.crud_csv = CRUD_CSV()

    def select_option_input(self):
        # Select an integer number from 1-5 as an option
        try:
            inpt = int(input("Enter you choice: "))
            if inpt > 0 and inpt < 6:
                return inpt
            else:
                print("Please select a valid input!")
        except ValueError:
            print("Please select a valid input!")

    def load_options(self):
        print(f"Loading student records from students.csv ... Done!")
        print(f"{"="*10} MENU {"="*10}")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Remove Student")
        print("5. Exit")
        print(f"{"="*20}")
        return self.select_option_input()
    
    def match_option(self, option):
        match option:
            case 1:
                print("Add new student")
                self.crud_csv.add_student('add_opt')
            case 2:
                print("View students list")
            case 3:
                print("Search student")
            case 4:
                print("Remove a student")
