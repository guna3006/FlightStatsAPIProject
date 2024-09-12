
import os
import subprocess

def install_requirements():
    if os.path.exists('requirements.txt'):
        subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])

if __name__ == "__main__":
    install_requirements()
