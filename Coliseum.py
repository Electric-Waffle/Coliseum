import subprocess
import os

chemin_vers_le_main_py = os.path.dirname(os.path.realpath(__file__)) + "\\ColiseumDependencies\\main.py"
subprocess.Popen(["python", chemin_vers_le_main_py])
