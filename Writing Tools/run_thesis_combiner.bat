@echo off
echo Thesis Combiner Script - Publication Ready Edition
echo ================================================

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

REM Run the script
echo.
echo Running the thesis combiner script...
python combine_thesis.py

echo.
if %ERRORLEVEL% equ 0 (
    echo Thesis combination completed successfully!
    echo.
    echo The combined document is saved at:
    echo C:\Users\roger\OneDrive\Desktop\Gauntlet_Projects\PROJECT-REVIEWS\()_SELF-ANALYSIS\AI Engineering Thesis\combined_thesis.docx
    echo.
    echo IMPORTANT: After opening the document in Word, right-click on the Table of Contents
    echo and select "Update Field" to ensure all entries are properly displayed.
) else (
    echo An error occurred while combining the thesis files.
    echo.
    echo Please make sure:
    echo 1. Python 3.6+ is installed and in your PATH
    echo 2. All required packages are installed (pip install -r requirements.txt)
    echo 3. The input directory exists and contains markdown files
)

pause 