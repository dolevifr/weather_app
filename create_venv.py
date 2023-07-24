import os
import subprocess
import sys

def main():
    venv_name = "myenv"  # Replace with the desired name for your virtual environment
    python_executable = sys.executable

    # Create the virtual environment
    subprocess.run([python_executable, "-m", "venv", venv_name])

    # Activate the virtual environment
    activate_script = f"{venv_name}/Scripts/activate" if sys.platform == "win32" else f"{venv_name}/bin/activate"
    subprocess.run([activate_script], shell=True)

    # Install packages from requirements.txt
    subprocess.run([f"{venv_name}/bin/pip", "install", "-r", "requirements.txt"])

    # Create and set up Django project
    django_admin = f"{venv_name}/Scripts/django-admin" if sys.platform == "win32" else f"{venv_name}/bin/django-admin"
    project_name = "myproject"  # Replace with your desired project name
    subprocess.run([django_admin, "startproject", project_name])

if __name__ == "__main__":
    main()
