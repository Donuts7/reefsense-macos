"""Setup configuration for creating the distribution."""
from setuptools import setup, find_packages

setup(
    name="reefsense",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'PyQt6>=6.0.0',
        'opencv-python>=4.5.0',
        'numpy>=1.19.0',
        'ultralytics>=8.0.0',
        'Pillow>=8.0.0',
        'matplotlib>=3.3.0',
        'pyinstaller>=5.0.0'
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'reefsense=main:main',
        ],
    },
)