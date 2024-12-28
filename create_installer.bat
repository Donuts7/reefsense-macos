@echo off
echo Creating Python virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing required packages...
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

echo Building executable...
python build_exe.py

echo Creating distribution folder...
if not exist "dist\reefsense\models" mkdir dist\reefsense\models

echo Copying model files...
if exist "models\*.pt" (
    copy models\*.pt dist\reefsense\models\
) else (
    echo Warning: No model files found in models directory
)

echo Creating zip archive...
cd dist
if exist "reefsense_windows.zip" del reefsense_windows.zip
tar -a -c -f reefsense_windows.zip reefsense
cd ..

echo.
echo Installation package created successfully!
echo The package is available at: dist\reefsense_windows.zip
echo.

pause