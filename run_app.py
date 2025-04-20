import os
import subprocess
import sys

def create_venv():
    """Create a virtual environment if it doesn't exist."""
    if not os.path.exists("venv"):
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        print("Virtual environment created.")

def install_requirements():
    """Install dependencies from requirements.txt."""
    print("Installing dependencies...")
    pip_path = os.path.join("venv", "bin", "pip") if os.name != "nt" else os.path.join("venv", "Scripts", "pip.exe")
    subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])
    print("Dependencies installed.")

def run_app():
    """Run the application."""
    print("Starting the application...")
    python_path = os.path.join("venv", "bin", "python") if os.name != "nt" else os.path.join("venv", "Scripts", "python.exe")
    subprocess.check_call([python_path, "app/src/app.py"])

if __name__ == "__main__":
    # Check if the virtual environment exists
    venv_exists = os.path.exists("venv")

    # Create the virtual environment if it doesn't exist
    if not venv_exists:
        create_venv()

    # Install requirements (always ensure dependencies are installed)
    install_requirements()

    # Run the application
    run_app()