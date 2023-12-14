from datetime import datetime, timedelta

REPORTS_LIST = ["download", "traffic-source", "device-model", "domain", "site", "second-level-domain",
    "language", "os-browser", "windows-browser", "browser", "windows-ie", "os", "windows", "ie", "device"]

AGENCY_LIST = ["agency-international-development", "agriculture", "commerce", "defense", "education", "energy",
    "environmental-protection-agency", "executive-office-president", "general-services-administration",
    "health-human-services", "homeland-security", "housing-urban-development", "interior", "justice", "labor",
    "national-aeronautics-space-administration", "national-archives-records-administration",
    "national-science-foundation", "nuclear-regulatory-commission", "office-personnel-management",
    "postal-db_service", "small-business-administration", "social-security-administration", "state", "transportation",
    "treasury", "veterans-affairs"]


def is_valid_date(date_string: str) -> bool:
    """
    Tests if a string is both a valid date, and is less than or equal to today's date.
    :param date_string: the user-provided date to test
    :return: true if valid, false if not
    """
    try:
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        today = datetime.today()
        if date_obj < (today - timedelta(days=7)):
            print("\n### Warning, API is currently only returning results for the last 7 days! ###\n")
        return date_obj <= today
    except ValueError:
        return False


def check_report_list(user_string: str) -> bool:
    """
    Tests if a user's input is contained within REPORTS_LIST.
    :param user_string: user's entry to validate
    :return: true if the input is in REPORTS_LIST, false if not
    """
    upper_reports_list = [report.upper() for report in REPORTS_LIST]
    no_hyphen_reports_list = [report.replace("-", " ") for report in upper_reports_list]
    # you might be wondering, Charles, why didn't you simply create the lists in all uppercase & without hyphens?
    # well... sometimes we do things without first thinking them through.
    if user_string.upper() in upper_reports_list or user_string.upper() in no_hyphen_reports_list:
        return True
    else:
        return False


def check_agency_list(user_string: str) -> bool:
    """
    Tests if a user's input is contained within AGENCY_LIST.
    :param user_string: user's entry you would like to validate
    :return: true if valid, false if not
    """
    upper_agency_list = [agency.upper() for agency in AGENCY_LIST]
    no_hyphen_agency_list = [agency.replace("-", " ") for agency in upper_agency_list]
    if user_string.upper() in upper_agency_list or user_string.upper() in no_hyphen_agency_list:
        return True
    else:
        return False


def get_yes_or_no(message: str) -> str:
    response = input(message).upper()
    valid_responses = ["YES", "NO"]
    while response not in valid_responses:
        response = input(message).upper()
    return response

