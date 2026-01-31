import os, csv, time

FILE_PATH = './students.csv'

CSV_HEADER = ['Name', 'Roll', 'Email', 'Department']


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

    def select_option_input(self):
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
        return self.select_option_input()
    