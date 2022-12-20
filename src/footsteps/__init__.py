import sys
import os
import subprocess
import shutil

initialized = False
output_dir_impl = None


def is_notebook() -> bool:
    # https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook
    try:
        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter

pip_list_process=None

def initialize(run_name=None, output_root="results/"):
    global pip_list_process

    try:
        subprocess.check_output(["git", "describe", "--always"], stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        raise Exception(
            "code that uses footsteps needs to be run in a git directory with at least one commit to record the git hash assosciated with this experiment"
        )

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
            if is_notebook():
                run_name = input()
            else:
                try:
                    import readline

                    def get_tab_completed_input(valid_completions):
                        readline.set_completer_delims(" \t\n;")
                        readline.parse_and_bind("tab: complete")
                        readline.set_completer(
                            lambda text, state: [
                                i for i in valid_completions if i.startswith(text)
                            ][state]
                        )
                        return input()

                    valid_completions = os.listdir(output_root)
                    run_name = get_tab_completed_input(valid_completions)
                except:
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
        f.write(sys.executable + "\n")
        f.write("Git Hash:\n")
        git_hash = (
            subprocess.check_output(["git", "describe", "--always"]).strip().decode()
        )
        f.write(git_hash + "\n")
        try:
            origin = (
                subprocess.check_output(["git", "remote", "get-url", "origin"])
                .strip()
                .decode()
            )
            if "github" in origin:
                f.write(origin + "/tree/" + git_hash + "\n")
        except:
            pass
        f.write("Uncommitted changes:\n")
        try:
            f.write(
                subprocess.check_output(
                    ["git", "diff", "HEAD", "--", ":^/*.ipynb"],
                    stderr=subprocess.DEVNULL,
                ).decode()
            )
        except subprocess.CalledProcessError as err:
            print("using fallback because your version of git is ancient")
            f.write(
                subprocess.check_output(["git", "diff", "HEAD", "--", "."]).decode()
            )
        f.write("Current working dir:\n")
        f.write(os.getcwd() + "\n")
        try:
            shutil.copy(sys.argv[0], output_dir_impl + os.path.basename(sys.argv[0]))
        except:
            pass
    try:
        with open(f"{output_dir_impl}package_versions.txt", "w") as f:
            pip_list_process = subprocess.Popen(
                [sys.executable, "-m", "pip", "list"], stdout=f, stderr=subprocess.DEVNULL
            )
    except:
        print("Pip list failed")


def __getattr__(name):
    if name == "output_dir":
        if not initialized:
            initialize()
        return output_dir_impl
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
