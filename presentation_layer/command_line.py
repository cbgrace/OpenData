import business
from exceptions import BusinessLogicException
import validation

"""
This module contains methods to retrieve input from the user and display data to the user via the command line. 

Methods:
--------
    get_report_name() -> str:
        Retrieves (and validates) the report name the user would like to search for, via the command line.
    get_agency_name() -> str:
        Retrieves (and validates) the agency name the user would like to search for, via the command line.
    get_date(report_name: str, agency_name: str) -> str:
        Retrieves (and validates) the date the user would like to search for, via the command line
    on_new_data(file_name=None, data_list=None):
        Prints out some information regarding the data being saved, asks user if they want to print the data, if yes, 
        prints data to the console. 
    on_old_data(file_name, data_list):
        Lets the user know where the data has already been saved, if the user chooses, displays the data to the console
    on_error(error_message=None):
        Prints a message to the console upon encountering an error.
    display_results(data_list):
        Takes a list (data_list), and prints that list line-by-line to the console.
    restart_program_check():
        Checks if the user would like to restart the program
    list_options(which_option):
        Displays a list of either all the report options, or all the agency options, so the user knows what they can search
    print_by_four(list):
        Takes a list and prints it four items at a time
    run():
        This is the function to call in main to start the program.

"""


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
    """
    Prints out some information regarding the data being saved, asks user if they want to print the data, if yes,
        prints data to the console.
    :param file_name: file name where the new data is saved
    :param data_list: list of data to potentially print
    :return: n/a
    """
    if file_name == None:  # call on_new_data with no params to print this message
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
    """
    Lets the user know where the data has already been saved, if the user chooses, displays the data to the console
    :param file_name: file name where the old data is saved
    :param data_list: list of data to potentially print
    :return: n/a
    """
    print(f"This data has been retrieved before, it exists in file: {file_name}")
    user_response = validation.get_yes_or_no("Would you like to print the data? :  ")
    if user_response == "NO":
        restart_program_check()
    elif user_response == "YES":
        display_results(data_list)

def on_error(error_message=None):
    """
    Prints a message to the console upon encountering an error.
    :param error_message: (optional) error message
    :return: n/a, calls restart_program_check()
    """
    print("Sorry, an error was encountered.")
    if error_message != None:
        print(error_message)
    restart_program_check()



def display_results(data_list):
    """
    Takes a list (data_list), and prints that list line-by-line to the console.
    :param data_list: list of data to print
    :return: n/a, calls restart_program_check()
    """
    if len(data_list) == 0:
        print("Looks like there was no data.")
    for line in data_list:
        print(f"{line}")
    restart_program_check()


def restart_program_check():
    """
    Checks if the user would like to restart the program
    :return: n/a
    """
    user_response = validation.get_yes_or_no("Would you like to restart the program? :  ")
    if user_response == "NO":
        print("Bye!")
    elif user_response == "YES":
        run()


def list_options(which_option):
    """
    Displays a list of either all the report options, or all the agency options, so the user knows what they can search
    :param which_option: either report or agency
    :return: n/a
    """
    if which_option == "report":
        print_by_four(validation.REPORTS_LIST)
    elif which_option == "agency":
        print_by_four(validation.AGENCY_LIST)


def print_by_four(list):
    """
    Takes a list and prints it four items at a time
    :param list: list to print
    :return: n/a
    """
    print()  # for a newline
    window_start = 0
    window_end = 4  # because it's not inclusive
    while len(list) > window_end:
        print("".join([f"{item}, " for item in list[window_start:window_end]]))
        window_start += 4
        window_end += 4
    print("".join([f"{item}, " for item in list[window_start:]]))
    print()  # for a newline


def run():
    """
    This is the function to call in main to start the program.
    :return: calls either business.check_current_files() or on_error()
    """
    report_name = get_report_name()
    if report_name == "LIST":
        list_options('report')
        report_name = get_report_name()
    if report_name == "EXIT":
        print('bye')
        exit()
    agency_name = get_agency_name()
    if agency_name == "LIST":
        list_options('agency')
        agency_name = get_agency_name()
    if agency_name == "EXIT":
        print('bye')
        exit()
    date = get_date(report_name, agency_name)
    try:
        return business.check_current_files(report_name, agency_name, date)
    except BusinessLogicException:
        return on_error()
