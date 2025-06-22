import sys
import platform
import subprocess
import pathlib
from pprint import pprint

APP_NAME = 'diochad'
ENTRY_SCRIPT = 'installer.py'

def run(command: list[str]) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(
            command, 
            check=True, 
            capture_output=True, 
            text=True
        )

    except subprocess.CalledProcessError as e:
        print(f'{command} failed its operation due to:')
        print(e.stderr)
        sys.exit(1)
    
    return result

def install_dependencies():
    # requiring uv package manager
    if run(['which', 'uv']).returncode != 0:
        print('please, install uv package manager first or create .venv folder for yourself.')
        sys.exit(1)

    # creating venv
    if not pathlib.Path('.venv').exists():
        result = run(['uv', 'venv']) 
        if result.returncode != 0:
            print('failed to create python virtual environment.')
            sys.exit(1) 

    # installing
    result = run(['uv', 'pip', 'install', '-r' 'requirements.txt'])
    if result.returncode != 0:
        print(f'failed to install dependencies.')
        pprint(result)
        sys.exit(1)
    else:
        print(f'dependencies succefully installed.')

def build_executable():

    cmd = [
        'uv', 'run',
        'pyinstaller',
        '--onefile',
        '--name', APP_NAME,
        '--clean',
        '--noconfirm',
        ENTRY_SCRIPT
    ]

    result = run(cmd) 
    if result.returncode != 0:
        print('failed to build executable')
        pprint(result)
        sys.exit(1)

def main():
    if platform.system() != 'Linux':
        print("Diochad only support Linux operating systems.")
        sys.exit(1)
    
    install_dependencies()
    build_executable() 

    print("Diochad installer succefully builded!") 

if __name__ == '__main__':
    main()