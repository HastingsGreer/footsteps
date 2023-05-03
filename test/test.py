import unittest
import filecmp
import shutil
import subprocess
import time
import sys

from subprocess import PIPE, Popen

import os.path


class FootstepsTestCase(unittest.TestCase):
    def testFootsteps(self):
        shutil.rmtree("results/my_results_name/", ignore_errors=True)
        output = subprocess.Popen(
            [sys.executable, "test/example_program.py", "horseradish"],
            stdin=PIPE,
            stdout=PIPE,
        ).communicate(b"my_results_name")

        self.assertTrue(os.path.exists("results/my_results_name/info.txt"))

        with open("results/my_results_name/info.txt", "r") as f:
            print("Current info format:\n=========================")
            print(f.read())
        time.sleep(5)
        with open("results/my_results_name/package_versions.txt", "r") as f:
            print("\n=========================\nCurrent packages format:\n=========================")
            package_file = f.read()
            print(package_file)
            self.assertTrue("footsteps" in package_file)

    def testCustomRoot(self):
        shutil.rmtree("../results/my_results_name/", ignore_errors=True)
        output = subprocess.Popen(
            [sys.executable, "test/example_custom_root.py", "horseradish"],
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
            [sys.executable, "test/example_program.py", "horseradish"],
            stdin=PIPE,
            stdout=PIPE,
        ).communicate(b"preexisting_results_name")
        output = subprocess.Popen(
            [sys.executable, "test/example_program.py", "horseradish"],
            stdin=PIPE,
            stdout=PIPE,
        ).communicate(b"preexisting_results_name")
        output = subprocess.Popen(
            [sys.executable, "test/example_program.py", "horseradish"],
            stdin=PIPE,
            stdout=PIPE,
        ).communicate(b"preexisting_results_name")

        self.assertTrue(os.path.exists("results/preexisting_results_name-2/info.txt"))


    def testSetNameUsingEnv(self):
        try:
            shutil.rmtree("results/my_results_name_env/", ignore_errors=True)
            os.environ["FOOTSTEPS_NAME"] = "my_results_name_env"
            output = subprocess.Popen(
                [sys.executable, "test/example_program.py", "horseradish"],
                stdin=PIPE,
                stdout=PIPE,
            ).communicate(b"")
            self.assertTrue(os.path.exists("results/my_results_name_env/info.txt"))
        finally:
            del os.environ["FOOTSTEPS_NAME"]
    def testNeedsGitDir(self):
        curr_dir = os.getcwd()
        try:
            os.chdir("..")
            import footsteps
            footsteps.initialize()
        finally:
            os.chdir(curr_dir)

    def testUncommittedFile(self):
        shutil.rmtree("results/uncommitted_file/", ignore_errors=True)

        try:
            shutil.copy("test/example_program.py", "test/example_uncommitted.py")

            output = subprocess.Popen(
                [sys.executable, "test/example_uncommitted.py"],
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
