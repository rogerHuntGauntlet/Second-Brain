Write-Host "Thesis Combiner Script - Publication Ready Edition" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python -V 2>&1
    if ($pythonVersion -match "Python (\d+\.\d+\.\d+)") {
        Write-Host "Found Python version: $($matches[1])" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "Python is not installed or not in PATH." -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.6 or higher from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "After installation, make sure to check 'Add Python to PATH' during installation." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Once Python is installed, run this script again." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit
}

# Check if requirements are installed
Write-Host "Checking and installing required packages..." -ForegroundColor Cyan
pip install -r requirements.txt

# Run the script
Write-Host ""
Write-Host "Running the thesis combiner script..." -ForegroundColor Cyan
python combine_thesis.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Thesis combination completed successfully!" -ForegroundColor Green
    Write-Host "The combined document is saved at:" -ForegroundColor Green
    Write-Host "C:\Users\roger\OneDrive\Desktop\Gauntlet_Projects\PROJECT-REVIEWS\()_SELF-ANALYSIS\AI Engineering Thesis\combined_thesis.docx" -ForegroundColor Green
    Write-Host ""
    Write-Host "IMPORTANT:" -ForegroundColor Yellow
    Write-Host "After opening the document in Word, right-click on the Table of Contents" -ForegroundColor Yellow
    Write-Host "and select 'Update Field' to ensure all entries are properly displayed." -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "An error occurred while combining the thesis files." -ForegroundColor Red
    Write-Host ""
    Write-Host "Please make sure:" -ForegroundColor Yellow
    Write-Host "1. Python 3.6+ is installed and in your PATH" -ForegroundColor Yellow
    Write-Host "2. All required packages are installed (pip install -r requirements.txt)" -ForegroundColor Yellow
    Write-Host "3. The input directory exists and contains markdown files" -ForegroundColor Yellow
}

Read-Host "Press Enter to exit" 