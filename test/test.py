import unittest
import filecmp
import shutil
import subprocess
import time

from subprocess import PIPE, Popen

import os.path


class FootstepsTestCase(unittest.TestCase):
    def testFootsteps(self):
        shutil.rmtree("results/my_results_name/", ignore_errors=True)
        output = subprocess.Popen(
            ["python", "test/example_program.py", "horseradish"],
            stdin=PIPE,
            stdout=PIPE,
        ).communicate(b"my_results_name")

        self.assertTrue(os.path.exists("results/my_results_name/info.txt"))

        with open("results/my_results_name/info.txt", "r") as f:
            print("Current info format:\n=========================")
            print(f.read())

    def testCustomRoot(self):
        shutil.rmtree("../results/my_results_name/", ignore_errors=True)
        output = subprocess.Popen(
            ["python", "test/example_custom_root.py", "horseradish"],
            stdin=PIPE,
            stdout=PIPE,
        ).communicate(b"my_results_name")

        self.assertTrue(os.path.exists("../results/my_results_name/info.txt"))
        self.assertTrue(os.path.exists("../results/my_results_name/card.txt"))

    def testFootstepsFallbackPath(self):
        shutil.rmtree("results/preexisting_results_name", ignore_errors=True)
        shutil.rmtree("results/preexisting_results_name-1", ignore_errors=True)
        shutil.rmtree("results/preexisting_results_name-2", ignore_errors=True)
        output = subprocess.Popen(
            ["python", "test/example_program.py", "horseradish"],
            stdin=PIPE,
            stdout=PIPE,
        ).communicate(b"preexisting_results_name")
        output = subprocess.Popen(
            ["python", "test/example_program.py", "horseradish"],
            stdin=PIPE,
            stdout=PIPE,
        ).communicate(b"preexisting_results_name")
        output = subprocess.Popen(
            ["python", "test/example_program.py", "horseradish"],
            stdin=PIPE,
            stdout=PIPE,
        ).communicate(b"preexisting_results_name")

        self.assertTrue(os.path.exists("results/preexisting_results_name-2/info.txt"))

    def testNeedsGitDir(self):
        curr_dir = os.getcwd()
        try:
            os.chdir("..")
            try:
                import footsteps

                raise Exception("Should have failed")
            except Exception as e:
                self.assertTrue(
                    str(e)
                    == "code that uses footsteps needs to be run in a git directory to record the git hash assosciated with this experiment"
                )

        finally:
            os.chdir(curr_dir)

    def testSetNameUsingEnv(self):
        try:
            shutil.rmtree("results/my_results_name_env/", ignore_errors=True)
            os.environ["FOOTSTEPS_NAME"] = "my_results_name_env"
            output = subprocess.Popen(
                ["python", "test/example_program.py", "horseradish"],
                stdin=PIPE,
                stdout=PIPE,
            ).communicate(b"")
            self.assertTrue(os.path.exists("results/my_results_name_env/info.txt"))
        finally:
            del os.environ["FOOTSTEPS_NAME"]

    def testUncommittedFile(self):
        shutil.rmtree("results/uncommitted_file/", ignore_errors=True)

        try:
            shutil.copy("test/example_program.py", "test/example_uncommitted.py")

            output = subprocess.Popen(
                ["python", "test/example_uncommitted.py"],
                stdin=PIPE,
                stdout=PIPE,
            ).communicate(b"uncommitted_file")
            self.assertTrue(
                filecmp.cmp(
                    "test/example_uncommitted.py",
                    "results/uncommitted_file/example_uncommitted.py",
                )
            )

        finally:

            os.remove("test/example_uncommitted.py")
