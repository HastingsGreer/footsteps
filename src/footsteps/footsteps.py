import sys
import os
import subprocess
import shutil

try:
    subprocess.check_output(["git", "status"], stderr=subprocess.PIPE)
except subprocess.CalledProcessError:
    raise Exception("code that uses footsteps needs to be run in a git directory to record the git hash assosciated with this experiment")
    
if "FOOTSTEPS_NAME" in os.environ:
    run_name = os.environ["FOOTSTEPS_NAME"]
else:
    print("Input name of experiment:")
    run_name = input()
output_dir = "results/" + run_name + "/"

suffix = 0
while os.path.exists(output_dir):
    suffix += 1
    output_dir = "results/" + run_name + "-" + str(suffix) + "/"

os.makedirs(output_dir)

with open(output_dir + "info.txt", "w") as f:
    f.write("Command:\n")
    f.write(" ".join(sys.argv) + "\n")
    f.write("System:\n")
    f.write(subprocess.check_output(["hostname"]).decode())
    f.write("Python:\n")
    f.write(shutil.which("python") + "\n")
    f.write("Git Hash:\n")
    f.write(
        subprocess.check_output(["git", "describe", "--always"]).strip().decode() + "\n"
    )
    f.write("Uncommitted changes:\n")
    f.write(
        subprocess.check_output(
            ["git", "diff", "HEAD", "--", ".", ":(exclude)*.ipynb"]
        ).decode()
    )
