import sys
import os
import subprocess
import shutil
import readline

try:
    subprocess.check_output(["git", "status"], stderr=subprocess.PIPE)
except subprocess.CalledProcessError:
    raise Exception("code that uses footsteps needs to be run in a git directory to record the git hash assosciated with this experiment")

# create directory "results/" if it doesn't exist
if not os.path.exists("results"):
    os.makedirs("results")

def get_tab_completed_input(valid_completions):
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(lambda text, state: [i for i in valid_completions if i.startswith(text)][state])
    return input()

print("Input name of experiment:")
valid_completions = os.listdir("results/")
# Often the user will want to enter similar names to the ones that are already in the results directory.
run_name = get_tab_completed_input(valid_completions)
output_dir = "results/" + run_name + "/"

suffix = 0
while os.path.exists(output_dir):
    suffix += 1
    output_dir = "results/" + run_name + "(" + str(suffix) + ")/"

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
