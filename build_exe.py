# """Build script to create executable."""
# import sys
# sys.path.append('C:\\Users\\pc\\AppData\\Roaming\\Python\\Python311\\Scripts')
# import pyinstaller.__main__ # type: ignore
# import os
# import sys
# import shutil

# def build_executable():
#     """Build the executable using PyInstaller."""
#     # Clean previous builds
#     if os.path.exists("dist"):
#         shutil.rmtree("dist")
#     if os.path.exists("build"):
#         shutil.rmtree("build")
        
#     # PyInstaller configuration
#     pyinstaller.__main__.run([
#         'main.py',
#         '--name=reefsense',
#         '--onedir',
#         '--windowed',
#         '--icon=src/gui/components/logo.png',
#         '--add-data=src/gui/components/logo.png:src/gui/components',
#         '--add-data=models:src/models',
#         '--hidden-import=PIL._tkinter_finder',
#         '--hidden-import=cv2',
#         '--hidden-import=ultralytics',
#         '--hidden-import=numpy',
#         '--hidden-import=PyQt6',
#         '--collect-all=ultralytics',
#         '--noconfirm'
#     ])

# if __name__ == "__main__":
#     build_executable()
import os
import sys
import shutil
import subprocess
import platform

def create_hook_file():
    """Create a custom hook file for Pydantic."""
    hook_content = """
from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = collect_all('pydantic')
hiddenimports += [
    'pydantic.json',
    'pydantic.dataclasses',
    'pydantic.datetime_parse',
    'pydantic.types',
    'pydantic.fields'
]
"""
    os.makedirs('hooks', exist_ok=True)
    with open('hooks/hook-pydantic.py', 'w') as f:
        f.write(hook_content)

# # def create_spec_file():

#     """Create a simplified PyInstaller spec file."""
#     spec_content = """# -*- mode: python ; coding: utf-8 -*-
# import sys
# sys.setrecursionlimit(sys.getrecursionlimit() * 5)

# block_cipher = None

# a = Analysis(
#     ['main.py'],
#     pathex=[],
#     binaries=[("D:/pc/Desktop/project-ai/noreact/new_venv/Scripts/python311.dll", 'python311.dll')],
#     datas=[
#         ('src/gui/components/logo.png', 'src/gui/components'),
#         ('src/models', 'src/models')
#     ],
#     hiddenimports=[
#         'PIL._tkinter_finder',
#         'cv2',
#         'ultralytics',
#         'numpy',
#         'PyQt6',
#         'torch',
#         'torchvision',
#         'pydantic',
#       'pydantic.typing'
#     ],
#     hookspath=['hooks'],
#     hooksconfig={},
#     runtime_hooks=[],
#     excludes=[],
#     win_no_prefer_redirects=False,
#     win_private_assemblies=False,
#     cipher=block_cipher,
#     noarchive=False,
# )

# pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# exe = EXE(
#     pyz,
#     a.scripts,
#     [],
#     exclude_binaries=True,
#     name='reefsense',
#     debug=False,
#     bootloader_ignore_signals=False,
#     strip=False,
#     upx=True,
#     console=True,
#     disable_windowed_traceback=False,
#     target_arch=None,
#     codesign_identity=None,
#     entitlements_file=None,
#     icon=['src/gui/components/logo.png']
# )

# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='reefsense'
# )
# """
#     with open('reefsense.spec', 'w') as f:
#         f.write(spec_content)

def create_spec_file():
    """Create a simplified PyInstaller spec file."""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(sys.getrecursionlimit() * 5)

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[
        ("D:/pc/Desktop/project-ai/noreact/new_venv/Scripts/python311.dll", ".")  # Place at root of dist folder
    ],
    datas=[
        ('src/gui/components/logo.png', 'gui/components'),  # Customize destination folder
        ('src/models', 'models')  # Customize destination folder
    ],
    hiddenimports=[
        'PIL._tkinter_finder',
        'cv2',
        'ultralytics',
        'numpy',
        'PyQt6',
        'torch',
        'torchvision',
        'pydantic',
        'pydantic.typing'
    ],
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='reefsense',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src/gui/components/logo.png'  # Use a valid icon path
)

coll = COLLECT(
    exe,
    a.binaries,  # Include binaries without nesting under _internal
    a.zipfiles,
    a.datas,  # Include datas without nesting under _internal
    strip=False,
    upx=True,
    upx_exclude=[],
    name='reefsense'
)
"""
    with open('reefsense.spec', 'w') as f:
        f.write(spec_content)


def setup_environment():
    """Set up the virtual environment and install requirements."""
    print("Setting up build environment...")
    
    # Create and activate virtual environment
    if not os.path.exists("build_venv"):
        subprocess.run([sys.executable, "-m", "venv", "build_venv"], check=True)
    
    # Get the proper pip and python commands based on platform
    if platform.system() == "Windows":
        python_path = os.path.join("build_venv", "Scripts", "python.exe")
        pip_path = os.path.join("build_venv", "Scripts", "pip.exe")
    else:
        python_path = os.path.join("build_venv", "bin", "python")
        pip_path = os.path.join("build_venv", "bin", "pip")
    
    # Install packages in a specific order
    print("Installing required packages...")
    packages = [
        "pip>=21.0",
        "wheel>=0.37.0",
        "setuptools>=65.5.1",
        "pyinstaller==5.13.2",  # Using a specific stable version
        "numpy>=1.19.0",
        "Pillow>=8.0.0",
        "PyQt6>=6.0.0",
        "opencv-python>=4.5.0",
        "pydantic==1.10.13",  # Using V1 to avoid V2 compatibility issues
        "ultralytics>=8.0.0",
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "matplotlib>=3.3.0"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.run([pip_path, "install", package], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package}: {e}")
            raise
    
    return python_path

def build_executable():
    """Build the executable using PyInstaller with spec file."""
    print("Building executable...")
    
    # Clean previous builds
    for dir_name in ["dist", "build"]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    # Create hook file and spec file
    create_hook_file()
    create_spec_file()
    
    # Build using spec file
    subprocess.run(["pyinstaller", "reefsense.spec", "--noconfirm"], check=True)

def create_distribution():
    """Create the final distribution package."""
    print("Creating distribution package...")
    
    # Create zip file
    base_name = "reefsense_windows" if platform.system() == "Windows" else "reefsense_linux"
    shutil.make_archive(
        os.path.join("dist", base_name),
        "zip",
        "dist/reefsense"
    )

def main():
    """Main build process."""
    try:
        # Clean up any existing files
        for item in ["build_venv", "dist", "build", "hooks", "*.spec"]:
            if os.path.exists(item):
                if os.path.isdir(item):
                    shutil.rmtree(item)
                else:
                    os.remove(item)
        
        python_path = setup_environment()
        build_executable()
        create_distribution()
        print("\nBuild completed successfully!")
        print(f"Distribution package available in the 'dist' folder")
    except Exception as e:
        print(f"\nError during build process: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()