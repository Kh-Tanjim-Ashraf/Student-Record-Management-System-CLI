from crud_student_data import LoadCSV

def main():
    load_csv = LoadCSV()
    while True:
        if load_csv.load_options() == 5:
            break


if __name__ == "__main__":
    main()