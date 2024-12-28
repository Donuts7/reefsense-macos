# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(sys.getrecursionlimit() * 5)

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[("D:/pc/Desktop/project-ai/noreact/new_venv/Scripts/python311.dll", '.')],
    datas=[
        ('src/gui/components/logo.png', 'src/gui/components'),
        ('src/models', 'src/models'),
        ('src/gui/components/logo.svg', 'src/gui/components'),  # Added logo.svg
        ('src/gui/styles/down_arrow.png', 'src/gui/styles'),  # Added down_arrow.png
        ('src/gui/styles/up_arrow.png', 'src/gui/styles'),    # Added up_arrow.png
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
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['src/gui/components/logo.png']
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='reefsense'
)
