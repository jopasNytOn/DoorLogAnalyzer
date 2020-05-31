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
2020-02-07 10:51:32.744 (9): Close door requested\n\
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
2020-02-12 05:05:32.030 (8): Close door requested\n\
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
2020-02-17 13:43:34.376 (8): Close door requested\n\
---\n\
\n\
\n\
Found 1 problem\
'

printing_log_OnlyOneHeaderRow = '\
Found 14 rows altogether\n\
\n\
\n\
2020-03-29 10:22:43.925 (7): Door at fully open position\n\
2020-03-29 10:23:41.979 (2): Close door requested\n\
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


if __name__ == '__main__':
    unittest.main()

