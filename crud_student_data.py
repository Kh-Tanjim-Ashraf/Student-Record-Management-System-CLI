import os, csv, time, re

FILE_PATH = './students.csv'

NEW_FILE_PATH = './updated_student.csv'

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
    
    def student_list(self):
        with open(FILE_PATH, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for index, row in enumerate(csv_reader):
                print(f"{index+1}. Name: {row.get('Name')}")
                print(f"Roll: {row.get('Roll')}")
                print(f"Email: {row.get('Email')}")
                print(f"Department: {row.get('Department')} \n")
            print(f"{"\n"*2}")
    
    def remove_student_confirmation(self, roll):
        with open(FILE_PATH, mode='r', encoding='utf-8') as csv_file:
            csv_file = csv.DictReader(csv_file)
            for row in csv_file:
                if row.get('Roll') == f"{roll}":
                    x = input(f"Are you sure you want to delete student with roll number {row.get('Roll')}? (y/n): ")
                    if x.isalpha() and (x.lower() == "y" or x.lower() == "yes"):
                        return True
                    else:
                        return False
                else:
                    print(f"Error: Student with the roll number {roll} does not exist!")            
    
    def remove_student(self, roll):
        # Open the file in both read & write mode using the same 'with' block since the file.
        # Mental Model: Rewrite the rows in a separate file without the specified row, since literal deletion doesn't work on CSV file.
        with open(FILE_PATH, mode='r', encoding='utf-8') as csv_file_read, \
            open(NEW_FILE_PATH, mode='w', newline='', encoding='utf-8') as csv_file_write:
            csv_reader = csv.DictReader(csv_file_read)
            csv_writer = csv.DictWriter(csv_file_write, fieldnames=CSV_HEADER)

            # Create header in the new CSV file
            csv_writer.writeheader()

            for row in csv_reader:
                # Write every row from old to new CSV file except the matched roll number
                if row.get('Roll') != f"{roll}":
                    csv_writer.writerow(row)
        
        # Remove the old file & rename the new file with the old file name to maintain consistency
        os.remove(FILE_PATH)
        os.rename(NEW_FILE_PATH, FILE_PATH)
    
    def open_csv_and_loop_search(self, searching_criteria, value):
        with open(FILE_PATH, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            if searching_criteria == "Roll":
                for row in csv_reader:
                    if value.lower() in row.get('Roll').lower():
                        return row
            elif searching_criteria == "Email":
                for row in csv_reader:
                    if value in row.get('Email').lower():
                        return row
            else:
                for row in csv_reader:
                    if value.lower() in row.get('Name').lower():
                        return row

    def search_student(self):
        x = input("Enter search term (name/email/roll): ")
        data = dict()
        if x:
            try:
                int(x)
                data = self.open_csv_and_loop_search("Roll", x)
            except ValueError:
                email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
                email = re.fullmatch(email_pattern, x)
                if email is not None:
                    data = self.open_csv_and_loop_search("Email", email.string)
                else:
                    data = self.open_csv_and_loop_search("Name", x)

            if data:
                print("Search Result:")
                print(f"Name: {data.get('Name')}")
                print(f"Roll: {data.get('Roll')}")
                print(f"Email: {data.get('Email')}")
                print(f"Department: {data.get('Department')}")
            else:
                print("No student record is found!")
        else:
            print("Empty input is not allowed!")
            self.search_student()




class LoadCSV:
    def __init__(self):
        if os.path.exists(FILE_PATH):
            print("Welcome to the Student Record Management System!")
            print("Loading student records from students.csv ... Done!")
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
                self.crud_csv.student_list()
            case 3:
                print("Search student")
                self.crud_csv.search_student()
            case 4:
                print("Remove a student")
                try:
                    x = int(input("Enter the roll number of the student to delete: "))
                    if self.crud_csv.remove_student_confirmation(x):
                        self.crud_csv.remove_student(x)
                        print("Student record deleted successfully!")
                except ValueError:
                    print("Enter a valid roll number. Hint: Integer Number")
