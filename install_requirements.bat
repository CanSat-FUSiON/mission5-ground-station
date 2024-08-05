@echo off
REM This batch file installs Python packages listed in requirements.txt

REM Check if requirements.txt exists
IF NOT EXIST requirements.txt (
    echo requirements.txt not found!
    exit /b 1
)

REM Install the packages using pip
echo Installing packages from requirements.txt...
pip install -r requirements.txt

REM Check if the installation was successful
IF %ERRORLEVEL% EQU 0 (
    echo Installation completed successfully!
) ELSE (
    echo Installation failed. Check the error messages above.
)

pause
