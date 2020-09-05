from datetime import datetime
from openpyxl import load_workbook
import sys
import time

if len(sys.argv) != 2:
    sys.exit('Version 0.05, Usage: DoorLogAnalyzer <csv-file / xlsx-file>')

def convert_date_string_to_date_timestamp(date_string):
    date_object = None
    try:
        date_object = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
    except ValueError:
        try:
            date_object = datetime.strptime(date_string, '%d/%m/%Y %H:%M:%S')
        except ValueError:
            pass
    return time.mktime(date_object.timetuple())

maximum_seconds_to_request_close = 30


class File():
    def __init__(self, filename):
        self.filename = filename

        # First a couple of rows contain special text that are ignored.
        # The data is read from last to first row due to ascending time.
        self.row = 1

    def data_remains(self):
        self.row -= 1
        return self.row != self.last_special_row

    def get_row(self):
        return self.row


class CSVFile(File):
    def __init__(self, filename):
        super().__init__(filename)

        self.lines = []
        self.last_special_row = self.row - 1
        file = open(filename, 'r')
        for line in file:
            line = line.strip()
            self.lines.append(line)
            self.row += 1
        self.row -= 1

        print('Found {} rows altogether'.format(self.row))

    def get_data_from_cell(self, column, row):
        line = self.lines[row]
        column = int(column, 16) - int('A', 16)
        return self.get_substring(line, ";", column)

    def get_date(self):
        date = self.get_data_from_cell('E', self.row)
        return date, convert_date_string_to_date_timestamp(date)

    def get_message(self):
        return self.get_data_from_cell('D', self.row)

    def get_substring(self, string, delimiter, count):
        while count > 0:
            string = string[string.find(delimiter) + 1:]
            count -= 1
        string = string[:string.find(delimiter)]
        return string


class ExcelFile(File):
    def __init__(self, filename):
        super().__init__(filename)

        self.wb = load_workbook(filename=self.filename)
        self.sheet = self.wb['Sheet 1']

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

    def get_date(self):
        date = self.get_data_from_cell('A', self.row)
        return date, convert_date_string_to_date_timestamp(date)

    def get_message(self):
        return self.get_data_from_cell('D', self.row)


class Message():
    def __init__(self, input_file):
        self.row = input_file.get_row()
        self.date, self.datetime = input_file.get_date()
        self.message = input_file.get_message()

    def is_jam_starting(self):
        return self.message == 'Door at fully open position'

    def is_needed_more_time_to_keep_open(self):
        return self.message == 'Open door requested' or self.message == 'Photo cell'

    def is_jam_ending(self):
        return self.message == 'Door is closing and is at or below 50 mm from fully closed position' or \
               self.message == 'Door has stopped'


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
        print('{} ({}): {}'.format(self.ending_message.date, self.ending_message.row, self.ending_message.message))
        print('---')


def collect_jams(filename):
    problems = 0
    active_jam = Jam(None)
    input_file = None

    if filename.find("xlsx") > 0:
        input_file = ExcelFile(filename)
    elif filename.find("csv") > 0:
        input_file = CSVFile(filename)

    while input_file.data_remains():
        message = Message(input_file)
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
            elif message.message == 'Door has stopped':
                continue
            active_jam = Jam(None)

    return problems


problems = collect_jams(sys.argv[1])
plural = "" if problems == 1 else "s"
print('\n\nFound {} problem{}'.format(problems, plural))
