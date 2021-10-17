import unittest
import subprocess
import time

from subprocess import PIPE, Popen

import os.path

class FootstepsTestCase(unittest.TestCase):
    def testFootsteps(self):
        output = subprocess.Popen(["python", "test/example_program.py", "horseradish"], stdin=PIPE, stdout=PIPE).communicate("my_results_name")
        
        self.assertTrue(os.path.exists("results/my_results_name/info.txt")
        
        
