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
    subprocess.check_call([os.path.join("venv", "bin", "pip"), "install", "-r", "requirements.txt"])
    print("Dependencies installed.")

def run_app():
    """Run the application."""
    print("Starting the application...")
    subprocess.check_call([os.path.join("venv", "bin", "python"), "app/src/app.py"])

if __name__ == "__main__":
    create_venv()
    install_requirements()
    run_app()