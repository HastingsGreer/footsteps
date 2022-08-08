[<img src="https://github.com/HastingsGreer/footsteps/actions/workflows/test.yml/badge.svg">](https://github.com/HastingsGreer/footsteps/actions) [<img src="https://img.shields.io/pypi/v/footsteps.svg?color=blue">](https://pypi.org/project/footsteps/)
## Footsteps

A non-configurable experiment logging package.

Footsteps provides an output directory pre-filled with `info.txt` describing your code and the circumstances in which it is running, so that it takes minimal effort to keep track of what code generated what result, even if you are writing a five line throwaway script. Then, 3 years later when you are trying to understand how you generated that figure or trained that network, you have enough information to follow your footsteps and work out exactly what you did.

By default, when your code asks footsteps for an output directory, the user is prompted for an experiment name. Much like git commit messages, this seems like it would be annoying, but I've found it to be worthwhile.

```bash
[hastings@$Hastingss-Air ~/sample_project]$ pip install footsteps
...
[hastings@$Hastingss-Air ~/sample_project]$ cat sample_project.py
import footsteps

with open(footsteps.output_dir + "network_weights.csv", "w") as f:
    f.write("6, 9, 42")

[hastings@$Hastingss-Air ~/sample_project]$ python sample_project.py
Input name of experiment:
manually_entered_experiment_name
Saving results to results/manually_entered_experiment_name/

[hastings@$Hastingss-Air ~/sample_project]$ cat results/manually_entered_experiment_name/info.txt
Command:
sample_project.py
System:
Hastingss-Air
Python:
/Users/hastings/opt/anaconda3/bin/python
Git Hash:
288b9ca
Uncommitted changes:
Current working dir:
/Users/hastings/sample_project
```
Footsteps can also be told to log to a programatically determined experiment name with `initialize`. This is useful for unit tests and such.
```
[hastings@$Hastingss-Air ~/sample_project]$ sed 's/^$/footsteps.initialize("fixed_experiment_name")/' sample_project.py | tee sample_project.py
import footsteps
footsteps.initialize("fixed_experiment_name")
with open(footsteps.output_dir + "network_weights.csv", "w") as f:
    f.write("6, 9, 42")

[hastings@$Hastingss-Air ~/sample_project]$ python sample_project.py --finnicky-command-line-argument
Saving results to results/fixed_experiment_name/

[hastings@$Hastingss-Air ~/sample_project]$ cat results/fixed_experiment_name/info.txt
Command:
sample_project.py --finnicky-command-line-argument
System:
Hastingss-Air
Python:
/Users/hastings/opt/anaconda3/bin/python
Git Hash:
288b9ca
Uncommitted changes:
diff --git a/sample_project.py b/sample_project.py
index 9dea213..4ec6cca 100644
--- a/sample_project.py
+++ b/sample_project.py
@@ -1,4 +1,4 @@
 import footsteps
-
+footsteps.initialize("fixed_experiment_name")
 with open(footsteps.output_dir + "network_weights.csv", "w") as f:
     f.write("6, 9, 42")
Current working dir:
/Users/hastings/sample_project
```
If you re-use an experiment name, the old one will never be overwritten: instead, a numeral is added to disambiguate:
```
[hastings@$Hastingss-Air ~/sample_project]$ python sample_project.py
Saving results to results/fixed_experiment_name-1/
```

    


### Philosophy

Experiment reproduction is hard at two points in time: First, when doing an experiment, it is easy to lack the motivation to meticulously record what you are doing, including details such as package versions or code changes that you may not think are important. Second, when trying to reproduce an experiment, motivation is available in abundance, but the information needed may no longer exist.

To solve this problem, footsteps is designed to require as little motivation as possible at experiment time, and to provide as much information as possible at reproduction time.

### Usage Details

To use footsteps, just import the package. At runtime, this will prompt the user for a descriptive name to be assosciated with any artifacts generated by this iteration of your code. Tab completion is available for the experiment name if you want to use a name parallel with previous names. Then, it will create a directory using that name, dump information into "info.txt" in that directory including the current git hash, command and arguments, which python env is in use etc into that directory. Versions of installed packages are dumped into the output directory in the file "package_versions.txt" using `pip list` (specifically `Popen([sys.executable, "-m", "pip", "list"])`), which correctly records versions of packages whether they are installed with conda or pip. Finally, the path to this directory is available as `footsteps.output_dir`, so that the rest of your code knows where to put any artifacts that it generates.

In the event that a project using footsteps grows to the point where you want to configure or specialize footsteps, the recommended process is to copy footsteps/footsteps.py into your codebase, modify it to make any changes you need, and import that instead of this.

