import validation

def get_report_name() -> str:
    user_response = input("Report Name: ")
    while not validation.check_report_list(user_response):
        print('Invalid report name!')
        user_response = input("Report Name: ")
    return user_response

def get_agency_name() -> str:
    user_response = input("Agency Name: ")
    while not validation.check_agency_list(user_response):
        print(f"{user_response} is not a vaild agency, please try again.")
        user_response = input("Agency Name: ")
    return user_response

def get_date(report_name: str, agency_name: str) -> str:
    user_response = input(f"Date of {report_name} for {agency_name} in YYYY-MM-DD format: ")
    while not validation.is_valid_date(user_response):
        print(f"{user_response} is not a vaild date, please try again.")
        user_response = input(f"Date of {report_name} for {agency_name} in YYYY-MM-DD format: ")
    return user_response

def run():
    report_name = get_report_name()
    agency_name = get_agency_name()
    date = get_date(report_name, agency_name)
    print(report_name, agency_name, date)