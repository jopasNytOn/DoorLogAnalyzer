import subprocess
import unittest

def call_command(command):
    return subprocess.check_output(command, shell=True).rstrip().decode("utf-8")

printing_log_ok = '\
Found 17 rows altogether\n\
\n\
\n\
Found 0 problems\
'

printing_log_2020_02_12_07_00 = '\
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

printing_log_2020_02_17_15_43 = '\
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


class TestDoorLogAnalyzer(unittest.TestCase):

    def test_log_ok(self):
        value = call_command("python DoorLogAnalyzer.py test/Log_ok.xlsx")
        self.assertEqual(printing_log_ok, value)

    def test_log_2020_02_12_07_00(self):
        value = call_command("python DoorLogAnalyzer.py test/Log_2020-02-12_07-00.xlsx")
        self.assertEqual(printing_log_2020_02_12_07_00, value)

    def test_log_2020_02_17_15_43(self):
        value = call_command("python DoorLogAnalyzer.py test/Log_2020-02-17_15-43.xlsx")
        self.assertEqual(printing_log_2020_02_17_15_43, value)


if __name__ == '__main__':
    unittest.main()

