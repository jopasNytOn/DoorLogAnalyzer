from datetime import datetime
from openpyxl import load_workbook
import sys
import time

if len(sys.argv) != 2:
    sys.exit('Version 0.03, Usage: DoorLogAnalyzer <xlsx-file>')

def convert_date_string_to_date_timestamp(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
    return time.mktime(date_object.timetuple())

maximum_seconds_to_request_close = 20


class ExcelFile():
    def __init__(self, filename):
        self.filename = filename
        self.wb = load_workbook(filename=self.filename)
        self.sheet = self.wb['Sheet 1']

        # First a couple of rows contain special text that are ignored.
        # The data is read from last to first row due to ascending time.
        self.row = 1
        if self.get_data_from_cell('A', 1) == "Time":
            self.row += 1
        try:
            if self.get_data_from_cell('A', 2) == "Column1":
                self.row += 1
        except ValueError:
            pass
        self.last_special_row = self.row - 1
        while self.get_data_from_cell('C', self.row) != None:
            self.row += 1
        self.row -= 1
        print('Found {} rows altogether'.format(self.row))

    def get_data_from_cell(self, column, row):
        return self.sheet['{}{}'.format(column, row)].value

    def data_remains(self):
        self.row -= 1
        return self.row != self.last_special_row

    def get_row(self):
        return self.row

    def get_date(self):
        date = self.get_data_from_cell('A', self.row)
        return date, convert_date_string_to_date_timestamp(date)

    def get_message(self):
        return self.get_data_from_cell('D', self.row)


class Message():
    def __init__(self, excel_file):
        self.row = excel_file.get_row()
        self.date, self.datetime = excel_file.get_date()
        self.message = excel_file.get_message()

    def is_jam_starting(self):
        return self.message == 'Door at fully open position'

    def is_needed_more_time_to_keep_open(self):
        return self.message == 'Open door requested' or self.message == 'Photo cell'

    def is_jam_ending(self):
        return self.message == 'Close door requested'


class Jam():
    def __init__(self, starting_message):
        self.starting_message = starting_message

    def increase_time(self, message):
        if self.starting_message:
            if message.datetime < self.starting_message.datetime + maximum_seconds_to_request_close:
                self.starting_message.datetime = message.datetime

    def end(self, message):
        if self.starting_message:
            if message.datetime >= self.starting_message.datetime + maximum_seconds_to_request_close:
                self.ending_message = message
                return True
        return False

    def print(self):
        print('{} ({}): Door at fully open position'.format(self.starting_message.date, self.starting_message.row))
        print('{} ({}): Close door requested'.format(self.ending_message.date, self.ending_message.row))
        print('---')


def collect_jams(excel_filename):
    excel_file = ExcelFile(excel_filename)

    problems = 0
    active_jam = Jam(None)
    while excel_file.data_remains():
        message = Message(excel_file)
        if message.is_jam_starting():
            active_jam = Jam(message)
        elif message.is_needed_more_time_to_keep_open():
            active_jam.increase_time(message)
        elif message.is_jam_ending():
            if active_jam.end(message):
                if problems == 0:
                    print('\n')
                active_jam.print()
                problems += 1
            active_jam = Jam(None)
    return problems


problems = collect_jams(sys.argv[1])
plural = "" if problems == 1 else "s"
print('\n\nFound {} problem{}'.format(problems, plural))
