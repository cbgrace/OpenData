from datetime import datetime

REPORTS_LIST = ["download", "traffic-source", "device-model", "domain", "site", "second-level-domain",
    "language", "os-browser", "windows-browser", "browser", "windows-ie", "os", "windows", "ie", "device"]

AGENCY_LIST = ["agency-international-development", "agriculture", "commerce", "defense", "education", "energy",
    "environmental-protection-agency", "executive-office-president", "general-services-administration",
    "health-human-services", "homeland-security", "housing-urban-development", "interior", "justice", "labor",
    "national-aeronautics-space-administration", "national-archives-records-administration",
    "national-science-foundation", "nuclear-regulatory-commission", "office-personnel-management",
    "postal-service", "small-business-administration", "social-security-administration", "state", "transportation",
    "treasury", "veterans-affairs"]


def is_valid_date(date_string: str) -> bool:
    try:
        # Attempt to parse the date string
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        # Check if the parsed date is today or earlier
        today = datetime.today()
        return date_obj <= today
    except ValueError:
        # If there's a ValueError, the date string is not a valid date
        return False


def check_report_list(user_string: str) -> bool:
    upper_reports_list = [report.upper() for report in REPORTS_LIST]
    no_hyphen_reports_list = [report.replace("-", " ") for report in upper_reports_list]
    if user_string.upper() in upper_reports_list or user_string.upper() in no_hyphen_reports_list:
        return True
    else:
        return False


def check_agency_list(user_string: str) -> bool:
    upper_agency_list = [agency.upper() for agency in AGENCY_LIST]
    no_hyphen_agency_list = [agency.replace("-", " ") for agency in upper_agency_list]
    if user_string.upper() in upper_agency_list or user_string.upper() in no_hyphen_agency_list:
        return True
    else:
        return False