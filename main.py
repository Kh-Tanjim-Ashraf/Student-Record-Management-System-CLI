from crud_student_data import LoadCSV

def main():
    load_csv = LoadCSV()
    while True:
        option = load_csv.load_options()
        # The loop will break if the user selects option 5, otherwise execute CRUD methods
        if option == 5:
            break
        else:
            load_csv.match_option(option)


if __name__ == "__main__":
    main()