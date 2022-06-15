import sys
import os
import subprocess
import shutil

try:
    subprocess.check_output(["git", "status"], stderr=subprocess.PIPE)
except subprocess.CalledProcessError:
    raise Exception(
        "code that uses footsteps needs to be run in a git directory to record the git hash assosciated with this experiment"
    )

initialized = False
output_dir_impl = None


def initialize(run_name=None, output_root="results/"):

    global output_dir_impl
    global initialized

    if initialized:
        raise Exception("footsteps can only be initialized once")

    initialized = True
    if not run_name:
        if "FOOTSTEPS_NAME" in os.environ:
            run_name = os.environ["FOOTSTEPS_NAME"]
        else:
            print("Input name of experiment:")
            run_name = input()
    output_dir_impl = os.path.join(output_root, run_name) + "/"

    suffix = 0
    while os.path.exists(output_dir_impl):
        suffix += 1
        output_dir_impl = os.path.join(output_root, run_name) + "-" + str(suffix) + "/"

    os.makedirs(output_dir_impl)

    print("Saving results to " + output_dir_impl)

    with open(output_dir_impl + "info.txt", "w") as f:
        f.write("Command:\n")
        f.write(" ".join(sys.argv) + "\n")
        f.write("System:\n")
        f.write(subprocess.check_output(["hostname"]).decode())
        f.write("Python:\n")
        f.write(shutil.which("python") + "\n")
        f.write("Git Hash:\n")
        f.write(
            subprocess.check_output(["git", "describe", "--always"]).strip().decode()
            + "\n"
        )
        f.write("Uncommitted changes:\n")
        f.write(
            subprocess.check_output(
                ["git", "diff", "HEAD", "--", ".", ":(exclude)*.ipynb"]
            ).decode()
        )
        f.write("Current working dir:\n")
        f.write(os.getcwd() + "\n")
        try:
            shutil.copy(sys.argv[0], output_dir_impl + os.path.basename(sys.argv[0]))
        except:
            pass


def __getattr__(name):
    if name == "output_dir":
        if not initialized:
            initialize()
        return output_dir_impl
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
