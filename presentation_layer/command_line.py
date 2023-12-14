import business
from exceptions import BusinessLogicException
import validation


def get_report_name() -> str:
    """
    Retrieves (and validates) the report name the user would like to search for, via the command line.
    :return: (str) the report name the user would like to search for
    """
    user_response = input("Report Name (enter 'list' to see all options, 'exit' to leave) : ")
    if user_response.upper() == "LIST" or user_response.upper() == "EXIT":
        return user_response.upper()
    else:
        while not validation.check_report_list(user_response):
            print('Invalid report name!')
            user_response = input("Report Name: ")
        return user_response


def get_agency_name() -> str:
    """
    Retrieves (and validates) the agency name the user would like to search for, via the command line.
    :return: (str) the agency name the user would like to search for
    """
    user_response = input("Agency Name (enter 'list' to see all options, 'exit' to leave) : ")
    if user_response.upper() == "LIST" or user_response.upper() == "EXIT":
        return user_response.upper()
    else:
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

def on_error(error_message=None):
    print("Sorry, an error was encountered.")
    if error_message != None:
        print(error_message)
    restart_program_check()



def display_results(data_list):
    if len(data_list) == 0:
        print("Looks like there was no data.")
    for line in data_list:
        print(f"{line}")
    restart_program_check()


def restart_program_check():
    user_response = validation.get_yes_or_no("Would you like to restart the program? :  ")
    if user_response == "NO":
        print("Bye!")
    elif user_response == "YES":
        run()


def list_options(which_option):
    if which_option == "report":
        print_by_four(validation.REPORTS_LIST)
    elif which_option == "agency":
        print_by_four(validation.AGENCY_LIST)


def print_by_four(list):
    print()  # just for a newline
    old_list = list.copy()
    new_list = []
    while len(old_list) >= 4:
        new_list.append(old_list[0])
        old_list.remove(old_list[0])
        if len(new_list) == 4:
            print(f"{new_list[0]}, {new_list[1]}, {new_list[2]}, {new_list[3]},")
            new_list.clear()
    # empty out the new list -- there is a better way to do this I will figure it out...
    if len(new_list) > 0:
        print("".join([f"{item}, " for item in new_list]))
    # else there are less than 4 items left, print them all!
    print("".join([f"{item}, " for item in old_list]))
    print()  # just for a newline


def run():
    report_name = get_report_name()
    if report_name == "LIST":
        list_options('report')
        report_name = get_report_name()
    elif report_name == "EXIT":
        return
    agency_name = get_agency_name()
    if agency_name == "LIST":
        list_options('agency')
        agency_name = get_agency_name()
    elif agency_name == "EXIT":
        return
    date = get_date(report_name, agency_name)
    try:
        return business.check_current_files(report_name, agency_name, date)
    except BusinessLogicException:
        return on_error()