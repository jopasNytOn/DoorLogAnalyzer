import subprocess
import unittest

def call_command(command):
    return subprocess.check_output(command, shell=True).rstrip().decode("utf-8")

printing_log_14SecondsLaterCloseDoorRequested = '\
Found 17 rows altogether\n\
\n\
\n\
Found 0 problems\
'

printing_log_20SecondsLaterCloseDoorRequested = '\
Found 18 rows altogether\n\
\n\
\n\
2020-02-07 10:51:12.680 (13): Door at fully open position\n\
2020-02-07 10:51:43.294 (6): Door is closing and is at or below 50 mm from fully closed position\n\
---\n\
\n\
\n\
Found 1 problem\
'

printing_log_DoorOpeningWithoutReachingFullyOpenPositionAfterNormalOpening = '\
Found 25 rows altogether\n\
\n\
\n\
Found 0 problems\
'

printing_log_OpenDoorRequestedBySafetyEdgeTriggered = '\
Found 54 rows altogether\n\
\n\
\n\
2020-02-11 23:59:26.898 (48): Door at fully open position\n\
2020-02-12 05:05:44.484 (5): Door is closing and is at or below 50 mm from fully closed position\n\
---\n\
\n\
\n\
Found 1 problem\
'

printing_log_OpenDoorRequestedWhenInFullyClosedPosition = '\
Found 42 rows altogether\n\
\n\
\n\
2020-02-17 13:13:00.875 (37): Door at fully open position\n\
2020-02-17 13:43:44.765 (5): Door is closing and is at or below 50 mm from fully closed position\n\
---\n\
\n\
\n\
Found 1 problem\
'

printing_log_OnlyOneHeaderRow = '\
Found 18 rows altogether\n\
\n\
\n\
2020-03-29 10:22:43.925 (11): Door at fully open position\n\
2020-03-29 10:23:52.427 (3): Door is closing and is at or below 50 mm from fully closed position\n\
---\n\
\n\
\n\
Found 1 problem\
'

printing_log_CsvFileWithDoorHasStopped = '\
Found 57 rows altogether\n\
\n\
\n\
25/07/2020 18:56:40 (38): Door at fully open position\n\
25/07/2020 19:08:18 (26): Door has stopped\n\
---\n\
\n\
\n\
Found 1 problem\
'

printing_log_CsvFileWithDoorMovedWhileJammed = '\
Found 16 rows altogether\n\
\n\
\n\
26/08/2020 10:16:26 (6): Door at fully open position\n\
26/08/2020 10:17:56 (4): Door has stopped\n\
---\n\
\n\
\n\
Found 1 problem\
'

printing_log_DoorJammedWhileClosing = '\
Found 14 rows altogether\n\
\n\
\n\
2020-09-25 12:52:33 (9): Door at fully open position\n\
2020-09-25 12:55:51 (3): Door is closing and is at or below 50 mm from fully closed position\n\
---\n\
\n\
\n\
Found 1 problem\
'


class TestDoorLogAnalyzer(unittest.TestCase):

    def test_log_14SecondsLaterCloseDoorRequested(self):
        value = call_command("python DoorLogAnalyzer.py test/Log_14SecondsLaterCloseDoorRequested.xlsx")
        self.assertEqual(printing_log_14SecondsLaterCloseDoorRequested, value)

    def test_log_20SecondsLaterCloseDoorRequested(self):
        value = call_command("python DoorLogAnalyzer.py test/Log_20SecondsLaterCloseDoorRequested.xlsx")
        self.assertEqual(printing_log_20SecondsLaterCloseDoorRequested, value)

    def test_log_DoorOpeningWithoutReachingFullyOpenPositionAfterNormalOpening(self):
        value = call_command("python DoorLogAnalyzer.py test/Log_DoorOpeningWithoutReachingFullyOpenPositionAfterNormalOpening.xlsx")
        self.assertEqual(printing_log_DoorOpeningWithoutReachingFullyOpenPositionAfterNormalOpening, value)

    def test_log_OpenDoorRequestedBySafetyEdgeTriggered(self):
        value = call_command("python DoorLogAnalyzer.py test/Log_OpenDoorRequestedBySafetyEdgeTriggered.xlsx")
        self.assertEqual(printing_log_OpenDoorRequestedBySafetyEdgeTriggered, value)

    def test_log_OpenDoorRequestedWhenInFullyClosedPosition(self):
        value = call_command("python DoorLogAnalyzer.py test/Log_OpenDoorRequestedWhenInFullyClosedPosition.xlsx")
        self.assertEqual(printing_log_OpenDoorRequestedWhenInFullyClosedPosition, value)

    def test_log_OnlyOneHeaderRow(self):
        value = call_command("python DoorLogAnalyzer.py test/Log_OnlyOneHeaderRow.xlsx")
        self.assertEqual(printing_log_OnlyOneHeaderRow, value)

    def test_log_CsvFileWithDoorHasStopped(self):
        value = call_command("python DoorLogAnalyzer.py test/Log_CsvFileWithDoorHasStopped.csv")
        self.assertEqual(printing_log_CsvFileWithDoorHasStopped, value)

    def test_log_CsvFileWithDoorMovedWhileJammed(self):
        value = call_command("python DoorLogAnalyzer.py test/Log_CsvFileWithDoorMovedWhileJammed.csv")
        self.assertEqual(printing_log_CsvFileWithDoorMovedWhileJammed, value)

    def test_log_DoorJammedWhileClosing(self):
        value = call_command("python DoorLogAnalyzer.py test/Log_DoorJammedWhileClosing.xlsx")
        self.assertEqual(printing_log_DoorJammedWhileClosing, value)

if __name__ == '__main__':
    unittest.main()

