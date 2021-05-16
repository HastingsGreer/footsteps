import sys
import os
import subprocess

print("Input name of run:")
run_name = input()
output_dir = "results/" + run_name + "/"

os.makedirs(output_dir)

with open(output_dir + "info.txt", "w") as f:
    f.write("Command:\n")
    f.write(" ".join(sys.argv) + "\n")
    f.write("System:\n")
    f.write(subprocess.check_output(["hostname"]).decode())
    f.write("Python:\n")
    f.write(subprocess.check_output(["which", "python"]).decode())
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
