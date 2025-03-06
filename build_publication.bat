@echo off
echo Publication Builder
echo =================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.6+ and try again.
    goto :end
)

REM Check if config file exists
if not exist publication_config.json (
    echo Warning: publication_config.json not found. Using default settings.
    python publication_builder.py
) else (
    python publication_builder.py --config publication_config.json
)

echo.
echo Done! Combined manuscript is available at Witt-Trans/combined_manuscript.md

:end
pause 