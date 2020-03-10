from datetime import datetime
from openpyxl import load_workbook
import sys
import time

if len(sys.argv) != 2:
    sys.exit('Version 0.01, Usage: DoorLogAnalyzer <xlsx-file>')

def convert_date_string_to_date_timestamp(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
    return time.mktime(date_object.timetuple())

maximum_seconds_to_request_close = 20

wb = load_workbook(filename = sys.argv[1])
sheet = wb['Sheet 1']

# First two rows contain special text that are ignored.
# The data is read from last to first row due to ascending time.
row = 3
while sheet['C{}'.format(row)].value != None:
    row += 1
row -= 1
print('Found {} rows altogether\n\n'.format(row))

problems = 0
saved_date = saved_timestamp = saved_row = None
while row != 2:
    if sheet['D{}'.format(row)].value == 'Door at fully open position':
        saved_date = sheet['A{}'.format(row)].value
        saved_timestamp = convert_date_string_to_date_timestamp(saved_date)
        saved_row = row
    elif sheet['D{}'.format(row)].value == 'Open door requested' or \
         sheet['D{}'.format(row)].value == 'Photo cell':
        if saved_date:
            tmp_date = sheet['A{}'.format(row)].value
            tmp_timestamp = convert_date_string_to_date_timestamp(tmp_date)
            if tmp_timestamp - saved_timestamp < maximum_seconds_to_request_close:
                saved_timestamp = tmp_timestamp
    elif sheet['D{}'.format(row)].value == 'Close door requested':
        if saved_date:
            new_date = sheet['A{}'.format(row)].value
            new_timestamp = convert_date_string_to_date_timestamp(new_date)
            if new_timestamp - saved_timestamp > maximum_seconds_to_request_close:
                print('{} ({}): Door at fully open position'.format(saved_date, saved_row))
                print('{} ({}): Close door requested'.format(new_date, row))
                print('---')
                problems += 1
        saved_date = saved_timestamp = saved_row = None
    row -= 1

print('\n\nFound {} problems'.format(problems))
