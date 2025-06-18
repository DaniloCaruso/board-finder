import os
import platform
import subprocess
import urllib.request

# URL of the Python script to download
PYTHON_SCRIPT_URL = "https://raw.githubusercontent.com/DaniloCaruso/board-finder/main/dev-board-finder.py"
TARGET_DIR = os.path.expanduser("~/.local/scripts/dev-board-finder")
TARGET_SCRIPT = os.path.join(TARGET_DIR, "dev-board-finder.py")
ALIAS_NAME = "dev-board-finder"
VENV_DIR = os.path.join(TARGET_DIR, "venv")

def create_directory():
    if not os.path.exists(TARGET_DIR):
        print(f"Creating directory {TARGET_DIR}...")
        os.makedirs(TARGET_DIR)

def create_virtualenv():
    if not os.path.exists(VENV_DIR):
        print(f"Creating virtual environment at {VENV_DIR}...")
        subprocess.check_call([os.sys.executable, "-m", "venv", VENV_DIR])

def install_requirements():
    print("Installing Python dependencies in virtual environment...")
    pip_executable = os.path.join(VENV_DIR, "bin", "pip") if platform.system() != "Windows" else os.path.join(VENV_DIR, "Scripts", "pip.exe")
    subprocess.check_call([pip_executable, "install", "tqdm"])

def download_script():
    print("Downloading the Python script...")
    urllib.request.urlretrieve(PYTHON_SCRIPT_URL, TARGET_SCRIPT)
    os.chmod(TARGET_SCRIPT, 0o755)

def add_alias():
    shell = os.getenv("SHELL")
    if "bash" in shell:
        shell_config_file = os.path.expanduser("~/.bashrc")
    elif "zsh" in shell:
        shell_config_file = os.path.expanduser("~/.zshrc")
    elif "fish" in shell:
        shell_config_file = os.path.expanduser("~/.config/fish/config.fish")
    else:
        print("Unsupported shell. Please add the alias manually.")
        return

    python_executable = os.path.join(VENV_DIR, "bin", "python3") if platform.system() != "Windows" else os.path.join(VENV_DIR, "Scripts", "python.exe")
    alias_command = f"alias {ALIAS_NAME}='{python_executable} {TARGET_SCRIPT}'"
    
    # Check if alias already exists in the config file
    alias_exists = False
    if os.path.exists(shell_config_file):
        with open(shell_config_file, "r") as f:
            content = f.read()
            if f"alias {ALIAS_NAME}=" in content:
                alias_exists = True
                print(f"Alias '{ALIAS_NAME}' already exists in {shell_config_file}")
    
    if not alias_exists:
        with open(shell_config_file, "a") as f:
            f.write(f"\n{alias_command}\n")
        print(f"Alias added to {shell_config_file}")
    else:
        print(f"Alias '{ALIAS_NAME}' already configured, skipping...")
    
    print("Reloading shell configuration...")
    try:
        subprocess.run(["/bin/bash", "-c", f"source {shell_config_file}"], check=True)
        print("Shell configuration reloaded successfully!")
    except subprocess.CalledProcessError:
        print(f"Could not reload shell configuration automatically. Please run: source {shell_config_file}")

def install():
    create_directory()
    create_virtualenv()
    install_requirements()
    download_script()
    add_alias()

if __name__ == "__main__":
    install()
