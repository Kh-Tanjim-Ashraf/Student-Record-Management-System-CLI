import os, csv, time, re

FILE_PATH = './students.csv'

NEW_FILE_PATH = './updated_student.csv'

CSV_HEADER = ['Name', 'Roll', 'Email', 'Department']

class CRUD_CSV:
    def __init__(self):
        pass

    def user_input(self) -> dict:
        """
        Take user input to add new student record
        """
        data = dict()
        usr_name = input("Enter student name: ").strip()

        if usr_name:
            uname_pattern = r"[a-zA-Z ]+"
            if re.fullmatch(uname_pattern, usr_name) != None:
                data["Name"] = usr_name
                usr_roll = input("Enter roll number: ").strip()
                if usr_roll:
                    try:
                        usr_roll = int(usr_roll)
                        data["Roll"] = usr_roll

                        usr_email = input("Enter email address: ").strip()
                        if usr_email:
                            email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
                            email = re.fullmatch(email_pattern, usr_email)
                            if email is not None:
                                data["Email"] = usr_email

                                usr_deprmnt = input("Enter department: ").strip()
                                if usr_deprmnt:
                                    data["Department"] = usr_deprmnt
                                else:
                                    print("Empty input is not allowed!")
                                    return None
                            else:
                                print("Please insert a valid email address!")
                                return None
                        else:
                            print("Empty input is not allowed!")
                            return None
                        
                    except ValueError:
                        print("Roll number must be an integer")
                        return None
                else:
                    print("Empty input is not allowed!")
                    return None
            else:
                print("Student name must be a string")
                return None
        else:
            print("Empty input is not allowed!")
            return None
        return data
        return {"Name" : usr_name, "Roll" : usr_roll, "Email" : usr_email, "Department": usr_deprmnt}
    
    def check_duplicate_roll_number(self, roll) -> bool:
        with open(FILE_PATH, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if row.get('Roll') == roll:
                    return True
            return False
        
    def add_student(self, data):
        """
        This function create new student record into the CSV file
        """
        with open(FILE_PATH, mode='a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADER)
            # Take user input
            data = self.user_input()
            if data != None:
                # Check for duplicate roll number, return True=Duplicate or False=Not Duplicate
                if self.check_duplicate_roll_number(data.get('Roll')):
                    print("Error: Roll number already exists for another student.")
                else:
                    # csv_writer.writerow(data)
                    print("Student record added successfully!")
    
    def student_list(self):
        """
        View all students list from the CSV file
        """
        with open(FILE_PATH, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for index, row in enumerate(csv_reader):
                print(f"{index+1}. Name: {row.get('Name')}")
                print(f"Roll: {row.get('Roll')}")
                print(f"Email: {row.get('Email')}")
                print(f"Department: {row.get('Department')} \n")
            print(f"{"\n"*2}")
    
    def remove_student_confirmation(self, roll):
        """
        This function initially checks if the student with such roll number exists & if found record then ask for confirmation before deleting the record from the CSV file.
        """
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
        """
        This function opens the CSV file in both read and write mode to rewrite the data while iterating each row except the specified roll number.
        """
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
    
    # Open CSV & execute search based on searching criteria
    def open_csv_and_loop_search(self, searching_criteria, value):
        """
        This function opens the CSV file & iterates each row based on the searching criteria.
        """
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
        """
        This function invokes the "open_csv_and_loop_search()" method based on the Name, Email or Roll number.
        """
        x = input("Enter search term (name/email/roll): ")
        data = dict()
        # Check if the input is not empty
        if x:
            # Mental model: If user inserts only integer value, make search by roll number. If it fails, then try to check if the input is a valid email, then search by email. If both does not bring any light, then search the CSV file based on the name criteria.
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
            # Show the result if the open & search through looping csv file returns any data
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
        print(f"\n {"="*10} MENU {"="*10}")
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
