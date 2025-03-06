@echo off
echo Wittgenstein Thesis Conversion to Word Format
echo ============================================
echo.

REM Set paths
set INPUT_FILE=Witt-Trans\combined_manuscript.md
set OUTPUT_FILE=Witt-Trans\wittgenstein_thesis.docx
set TITLE=The Language of Transaction: A Perspective on Wittgenstein
set AUTHOR=Roger B Hunt III

REM Move to Writing Tools directory where the script is located
cd "Writing Tools"

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH.
    echo.
    echo Please install Python 3.6 or higher from https://www.python.org/downloads/
    echo.
    echo After installation, make sure to check "Add Python to PATH" during installation.
    echo.
    echo Once Python is installed, run this batch file again.
    pause
    exit /b
)

REM Check if requirements are installed
echo Checking and installing required packages...
pip install -r requirements.txt

REM Run the script with custom parameters
echo.
echo Running the markdown to docx conversion script...
python combine_thesis.py --single-file="..\%INPUT_FILE%" --output="..\%OUTPUT_FILE%" --title="%TITLE%" --author="%AUTHOR%"

echo.
if %ERRORLEVEL% equ 0 (
    echo Conversion completed successfully!
    echo.
    echo The Word document is saved at:
    echo %cd%\..\%OUTPUT_FILE%
    echo.
    echo IMPORTANT: After opening the document in Word, right-click on the Table of Contents
    echo and select "Update Field" to ensure all entries are properly displayed.
) else (
    echo An error occurred while converting the file.
    echo.
    echo Please make sure:
    echo 1. Python 3.6+ is installed and in your PATH
    echo 2. All required packages are installed (pip install -r requirements.txt)
    echo 3. The input file exists
)

REM Return to original directory
cd ..

pause 