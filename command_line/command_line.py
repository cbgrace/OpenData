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

def run():
    """
    just for testing right now...
    :return:
    """
    report_name = get_report_name()
    agency_name = get_agency_name()
    date = get_date(report_name, agency_name)
    print(report_name, agency_name, date)
    return report_name, agency_name, date