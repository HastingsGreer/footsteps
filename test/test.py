import unittest
import subprocess
import time

from subprocess import PIPE, Popen

import os.path

class FootstepsTestCase(unittest.TestCase):
    def testFootsteps(self):
        output = subprocess.Popen(["python", "test/example_program.py", "horseradish"], stdin=PIPE, stdout=PIPE).communicate(b"my_results_name")
        
        self.assertTrue(os.path.exists("results/my_results_name/info.txt"))
        
        with open("results/my_results_name/info.txt", "r") as f:
            print("Current info format:\n=========================")
            print(f.read())
        
    def testFootstepsFallbackPath(self):
        output = subprocess.Popen(["python", "test/example_program.py", "horseradish"], stdin=PIPE, stdout=PIPE).communicate(b"preexisting_results_name")
        output = subprocess.Popen(["python", "test/example_program.py", "horseradish"], stdin=PIPE, stdout=PIPE).communicate(b"preexisting_results_name")
        output = subprocess.Popen(["python", "test/example_program.py", "horseradish"], stdin=PIPE, stdout=PIPE).communicate(b"preexisting_results_name")
        
        self.assertTrue(os.path.exists("results/preexisting_results_name-2/info.txt"))
        
    def testNeedsGitDir(self):
        curr_dir = os.getcwd()
        try:
            os.chdir("..")
            try:
                import footsteps
                raise Exception("Should have failed")
            except Exception as e:
                self.assertTrue(str(e) == "code that uses footsteps needs to be run in a git directory to record the git hash assosciated with this experiment")
        
        finally:
            os.chdir(curr_dir)

    def testSetNameUsingEnv(self):
        os.environ["FOOTSTEPS_NAME"] = "my_results_name"
        output = subprocess.Popen(["python", "test/example_program.py", "horseradish"], stdin=PIPE, stdout=PIPE).communicate(b"")
        self.assertTrue(os.path.exists("results/my_results_name/info.txt"))
