from command_line import run
import db_service
from datetime import datetime, date
import dal

if __name__ == '__main__':
    # this is all just testing I will create a business layer tomorrow...
    # first get info from user
    report_name = 'browser'
    agency_name = 'agriculture'
    date = '2023-12-10'
    # then see if the file already exists
    file_name = db_service.search_for_match(report_name, agency_name, date)
    # if this returns false, no file exists
    if file_name == False:
        # check if there is any data to add...
        today = datetime.today().date()
        params = {'before': f"{today}", 'after': f"{date}"}
        response = dal.make_request(report_name, agency_name, params=params)
        response = response.json()
        db_service.insert_search_data(agency_name, report_name, date)
        dal.save_json_to_txt(report_name, agency_name, date, response)
    else:
        data = dal.read_from_txt(report_name, agency_name, date)
        for line in data:
            print(line)