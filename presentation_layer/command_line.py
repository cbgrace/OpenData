import business
import validation


def get_report_name() -> str:
    """
    Retrieves (and validates) the report name the user would like to search for, via the command line.
    :return: (str) the report name the user would like to search for
    """
    user_response = input("Report Name: ")
    while not validation.check_report_list(user_response):
        print('Invalid report name!')
        user_response = input("Report Name: ")
    return user_response


def get_agency_name() -> str:
    """
    Retrieves (and validates) the agency name the user would like to search for, via the command line.
    :return: (str) the agency name the user would like to search for
    """
    user_response = input("Agency Name: ")
    while not validation.check_agency_list(user_response):
        print(f"{user_response} is not a vaild agency, please try again.")
        user_response = input("Agency Name: ")
    return user_response


def get_date(report_name: str, agency_name: str) -> str:
    """
    Retrieves (and validates) the date the user would like to search for, via the command line
    :param report_name: (str) report name already collected from the user
    :param agency_name: (str) agency name already collected from the user
    :return: (str) the date the user would like to search for
    """
    user_response = input(f"Date of {report_name} for {agency_name} in YYYY-MM-DD format: ")
    while not validation.is_valid_date(user_response):
        print(f"{user_response} is not a vaild date, please try again.")
        user_response = input(f"Date of {report_name} for {agency_name} in YYYY-MM-DD format: ")
    return user_response


def on_new_data(file_name=None, data_list=None):
    if file_name == None:
        print('This data has not been requested before, getting data...')
    else:
        print(f"Data retrieved, response saved to: {file_name}")
        # check if user wants to print results
        user_response = validation.get_yes_or_no("Would you like to print the data? :  ")
        if user_response == "NO":
            restart_program_check()
        elif user_response == "YES":
            display_results(data_list)


def on_old_data(file_name, data_list):
    print(f"This data has been retrieved before, it exists in file: {file_name}")
    user_response = validation.get_yes_or_no("Would you like to print the data? :  ")
    if user_response == "NO":
        restart_program_check()
    elif user_response == "YES":
        display_results(data_list)


def display_results(data_list):
    for line in data_list:
        print(f"{line}\n")
    restart_program_check()


def restart_program_check():
    user_response = validation.get_yes_or_no("Ok, would you like to restart the program? :  ")
    if user_response == "NO":
        print("Bye!")
    elif user_response == "YES":
        run()


def run():
    report_name = get_report_name()
    agency_name = get_agency_name()
    date = get_date(report_name, agency_name)
    return business.check_current_files(report_name, agency_name, date)
